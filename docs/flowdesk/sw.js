// "Servidor" do FlowDesk (a partir da Sprint 17): responde em api/ como um backend de verdade.
// Cada pedido passa antes pela rede de verdade (rede.json), então aparece na aba Rede e respeita a limitação de rede do navegador.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(self.clients.claim()));
const pergunta = async (clientId, msg) => {
  const c = clientId && await self.clients.get(clientId); if (!c) return null;
  return new Promise((r) => { const ch = new MessageChannel(); ch.port1.onmessage = (ev) => r(ev.data); c.postMessage(msg, [ch.port2]); setTimeout(() => r(null), 4000); });
};
const semAcento = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '');
const json = (o, st) => new Response(JSON.stringify(o), { status: st, headers: { 'Content-Type': 'application/json; charset=utf-8' } });
const espera = (ms) => new Promise((r) => setTimeout(r, ms));
self.addEventListener('fetch', (e) => {
  const u = new URL(e.request.url), i = u.pathname.indexOf('/api/');
  if (i < 0) return;
  const rota = u.pathname.slice(i + 5);
  e.respondWith((async () => {
    await fetch(new URL('rede.json?t=' + Date.now() + Math.random(), self.registration.scope), { cache: 'no-store' }).catch(() => {});
    await espera(220);
    if (rota === 'chamados' && e.request.method === 'POST') {
      const corpo = await e.request.json().catch(() => null);
      if (!corpo || !corpo.titulo || !String(corpo.titulo).trim() || !corpo.descricao || !String(corpo.descricao).trim()) return json({ erro: 'Título e descrição são obrigatórios' }, 400);
      const r = await pergunta(e.clientId || e.resultingClientId, { tipo: 'cria', chamado: corpo });
      return r ? json(r, 201) : json({ erro: 'Sem conexão com o FlowDesk' }, 503);
    }
    if (rota === 'chamados' && e.request.method === 'GET') {
      const r = await pergunta(e.clientId, { tipo: 'lista' }); if (!r) return json({ erro: 'Sem conexão com o FlowDesk' }, 503);
      const q = (u.searchParams.get('busca') || '').toLowerCase();
      // Sprint 17: o servidor tira o acento dos títulos, mas esquece de tirar o da busca
      const termo = r.bugAcento ? q : semAcento(q);
      return json(r.lista.filter((c) => semAcento(String(c.titulo).toLowerCase()).includes(termo)), 200);
    }
    return json({ erro: 'Rota não encontrada' }, 404);
  })());
});
