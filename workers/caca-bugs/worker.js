// Caça aos bugs do FlowDesk: recebe os reports, guarda e mostra o placar da temporada.
// Rotas: POST /envio · GET /placar?t=AAAA-MM · GET /admin?k=SENHA · POST /admin/decidir
const J = (o, s = 200, h = {}) => new Response(JSON.stringify(o), { status: s, headers: { 'content-type': 'application/json; charset=utf-8', ...h } });
const temporadaAtual = () => new Date().toISOString().slice(0, 7);
const limpa = (v, n) => String(v ?? '').replace(/[\u0000-\u001f\u007f]/g, ' ').trim().slice(0, n);
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const curto = (nome) => { const p = nome.split(/\s+/).filter(Boolean); return p.length > 1 ? `${p[0]} ${p[p.length - 1][0]}.` : p[0] || 'Aluno'; };

async function placar(env, t) {
  const p = (await env.CACA.get(`placar:${t}`, 'json')) || {};
  const linha = (await env.CACA.get(`linha:${t}`, 'json')) || [];
  return { temporada: t, bugs: [1, 2, 3].map((n) => (p[n] ? { n, ganhador: p[n].nome, quando: p[n].quando } : { n, ganhador: null })), encerrada: [1, 2, 3].every((n) => p[n]), envios: linha.slice(-40) };
}
// linha do tempo pública: quem mandou e quando (sem o conteúdo do report)
async function marcaLinha(env, t, e) {
  const l = (await env.CACA.get(`linha:${t}`, 'json')) || [];
  const i = l.findIndex((x) => x.recibo === e.id.slice(-8));
  const item = { recibo: e.id.slice(-8), nome: curto(e.nome), bug: e.bug, quando: e.quando, estado: e.estado };
  if (i >= 0) l[i] = item; else l.push(item);
  await env.CACA.put(`linha:${t}`, JSON.stringify(l.slice(-200)));
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url), cors = { 'access-control-allow-origin': env.ORIGEM, 'access-control-allow-headers': 'content-type', 'access-control-allow-methods': 'GET,POST' };
    if (req.method === 'OPTIONS') return new Response(null, { headers: cors });

    if (url.pathname === '/placar' && req.method === 'GET') {
      const t = /^\d{4}-\d{2}$/.test(url.searchParams.get('t') || '') ? url.searchParams.get('t') : temporadaAtual();
      return J(await placar(env, t), 200, { ...cors, 'cache-control': 'public, max-age=30' });
    }

    if (url.pathname === '/envio' && req.method === 'POST') {
      const ip = req.headers.get('cf-connecting-ip') || 'x';
      const chaveIp = `ip:${ip}`;
      if (await env.CACA.get(chaveIp)) return J({ ok: false, erro: 'Calma: espere um minuto antes de mandar outro.' }, 429, cors);
      let b; try { b = await req.json(); } catch { return J({ ok: false, erro: 'Envio inválido.' }, 400, cors); }
      const e = { nome: limpa(b.nome, 60), bug: +b.bug, passos: limpa(b.passos, 2000), esperado: limpa(b.esperado, 500), obtido: limpa(b.obtido, 500), evidencia: limpa(b.evidencia, 300), ambiente: limpa(b.ambiente, 200) };
      if (!e.nome || ![1, 2, 3].includes(e.bug) || e.passos.length < 15 || !e.esperado || !e.obtido) return J({ ok: false, erro: 'Preencha nome, passos, esperado e obtido.' }, 400, cors);
      const t = temporadaAtual(), id = `${Date.now()}-${crypto.randomUUID().slice(0, 8)}`;
      const novo = { ...e, id, t, quando: new Date().toISOString(), estado: 'pendente' };
      await env.CACA.put(`envio:${t}:${id}`, JSON.stringify(novo));
      await env.CACA.put(chaveIp, '1', { expirationTtl: 60 });
      await marcaLinha(env, t, novo);
      return J({ ok: true, id, recibo: id.slice(-8), quando: novo.quando }, 200, cors);
    }

    // o aluno confere o próprio envio pelo id completo (só ele tem): mostra o estado e, se ganhou, o código de vitória
    if (url.pathname === '/recibo' && req.method === 'GET') {
      const id = (url.searchParams.get('id') || '').replace(/[^\w-]/g, ''), t = id ? new Date(+id.split('-')[0]).toISOString().slice(0, 7) : '';
      const e = id && (await env.CACA.get(`envio:${t}:${id}`, 'json'));
      if (!e) return J({ ok: false }, 404, cors);
      return J({ ok: true, estado: e.estado, bug: e.bug, ganhou: !!e.codigo, codigo: e.codigo || null }, 200, cors);
    }

    // ---------- painel do professor ----------
    const k = url.searchParams.get('k') || '';
    if (url.pathname.startsWith('/admin')) {
      if (!env.ADMIN || k !== env.ADMIN) return new Response('Não autorizado', { status: 401 });
      const t = /^\d{4}-\d{2}$/.test(url.searchParams.get('t') || '') ? url.searchParams.get('t') : temporadaAtual();
      if (url.pathname === '/admin/decidir' && req.method === 'POST') {
        const f = await req.formData(), chave = `envio:${t}:${f.get('id')}`, e = await env.CACA.get(chave, 'json');
        if (e) {
          e.estado = f.get('acao') === 'aprovar' ? 'aprovado' : 'recusado';
          await env.CACA.put(chave, JSON.stringify(e));
          if (e.estado === 'aprovado') {
            const p = (await env.CACA.get(`placar:${t}`, 'json')) || {};
            if (!p[e.bug]) {
              e.codigo = 'VQA-' + crypto.randomUUID().replace(/-/g, '').slice(0, 6).toUpperCase();
              p[e.bug] = { nome: curto(e.nome), quando: e.quando, id: e.id, codigo: e.codigo }; await env.CACA.put(`placar:${t}`, JSON.stringify(p));
            }
          }
          await env.CACA.put(chave, JSON.stringify(e));
          await marcaLinha(env, t, e);
        }
        return Response.redirect(`${url.origin}/admin?k=${encodeURIComponent(k)}&t=${t}`, 303);
      }
      const lista = await env.CACA.list({ prefix: `envio:${t}:` });
      const envios = (await Promise.all(lista.keys.map((x) => env.CACA.get(x.name, 'json')))).filter(Boolean).sort((a, b) => a.quando.localeCompare(b.quando));
      const p = await placar(env, t);
      const linha = (e) => `<div class="e ${e.estado}"><div class="h"><b>Bug #${e.bug}</b> · ${esc(e.nome)} · ${new Date(e.quando).toLocaleString('pt-BR', { timeZone: 'America/Sao_Paulo' })} · <i>${e.estado}</i>${e.codigo ? ` · código <b>${e.codigo}</b>` : ''} · recibo ${e.id.slice(-8)}</div>
        <p><b>Passos</b><br>${esc(e.passos).replace(/\n/g, '<br>')}</p><p><b>Esperado:</b> ${esc(e.esperado)}</p><p><b>Obtido:</b> ${esc(e.obtido)}</p>${e.evidencia ? `<p><b>Evidência:</b> ${esc(e.evidencia)}</p>` : ''}${e.ambiente ? `<p><b>Ambiente:</b> ${esc(e.ambiente)}</p>` : ''}
        ${e.estado === 'pendente' ? `<form method="post" action="/admin/decidir?k=${encodeURIComponent(k)}&t=${t}"><input type="hidden" name="id" value="${e.id}"><button name="acao" value="aprovar">Aprovar</button> <button name="acao" value="recusar" class="r">Recusar</button></form>` : ''}</div>`;
      return new Response(`<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Caça aos bugs · ${t}</title>
<style>body{font-family:system-ui;background:#0b0c12;color:#eee;max-width:820px;margin:24px auto;padding:0 16px}.e{background:#14151f;border:1px solid #2a2c40;border-radius:12px;padding:14px 16px;margin:12px 0}.e.aprovado{border-color:#22c55e}.e.recusado{opacity:.5}.h{color:#a5a9bf;margin-bottom:6px}button{background:#7c3aed;color:#fff;border:0;border-radius:8px;padding:8px 14px;font-weight:700;cursor:pointer}button.r{background:#3a1218}</style>
<h1>Caça aos bugs · ${t}</h1><p>${p.bugs.map((b) => `Bug #${b.n}: ${b.ganhador ? '✅ ' + esc(b.ganhador) : '🔒 livre'}`).join(' · ')}</p>${envios.map(linha).join('') || '<p>Nenhum envio ainda.</p>'}`, { headers: { 'content-type': 'text/html; charset=utf-8' } });
    }
    return new Response('FlowDesk · caça aos bugs', { headers: cors });
  },
};
