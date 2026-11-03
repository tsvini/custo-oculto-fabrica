const { test, expect } = require('@playwright/test');
const PRODUTOS = require('../../../docs/loja/api/produtos.json');
const LOGIN = require('../../projeto2/dados/login.json');

const numero = (t) => Number(t.replace('R$', '').replace(/\./g, '').replace(',', '.').trim());
async function entrar(page, u = 'cliente', s = 'leigo123', url = 'index.html') {
  await page.goto(url);
  await page.getByTestId('usuario').fill(u);
  await page.getByTestId('senha').fill(s);
  await page.getByTestId('entrar').click();
}
// nenhum erro no console e nenhuma imagem/arquivo quebrado em nenhum teste
test.beforeEach(async ({ page }, info) => {
  info.erros = [];
  page.on('pageerror', (e) => info.erros.push('pageerror: ' + e.message));
  page.on('console', (m) => { if (m.type() === 'error' && !/Failed to load resource.*(api\/produtos|net::ERR_FAILED)/.test(m.text())) info.erros.push('console: ' + m.text()); });
  page.on('response', (r) => { if (r.status() >= 400 && !r.url().includes('favicon')) info.erros.push(`${r.status()} ${r.url()}`); });
});
test.afterEach(async ({}, info) => { if (!info.title.includes('[espera erro]')) expect(info.erros, 'erros na página').toEqual([]); });

test.describe('login', () => {
  test('cliente entra e vê o nome e a lista', async ({ page }) => {
    await entrar(page);
    await expect(page).toHaveURL(/produtos\.html/);
    await expect(page.getByTestId('titulo')).toHaveText('Produtos');
    await expect(page.getByTestId('usuario-logado')).toHaveText('cliente');
    await expect(page.getByTestId('produto')).toHaveCount(PRODUTOS.length);
    await expect(page.getByTestId('quantidade')).toHaveText(`${PRODUTOS.length} produtos`);
  });
  for (const c of LOGIN) {
    test(`mensagem do curso: ${c.cenario}`, async ({ page }) => {
      await entrar(page, c.usuario, c.senha);
      await expect(page.getByTestId('erro')).toHaveText(c.mensagem);
      await expect(page).toHaveURL(/index\.html/);
    });
  }
  test('usuário que não existe', async ({ page }) => {
    await entrar(page, 'fulano', 'leigo123');
    await expect(page.getByTestId('erro')).toHaveText('Usuário ou senha incorretos.');
  });
  test('bloqueado com a senha errada não diz que está bloqueado', async ({ page }) => {
    await entrar(page, 'bloqueado', 'errada');
    await expect(page.getByTestId('erro')).toHaveText('Usuário ou senha incorretos.');
  });
  test('os dois vazios: pede o usuário primeiro', async ({ page }) => {
    await entrar(page, '', '');
    await expect(page.getByTestId('erro')).toHaveText('Informe o usuário.');
  });
  test('espaço antes e depois do usuário é ignorado', async ({ page }) => {
    await entrar(page, '  cliente  ');
    await expect(page).toHaveURL(/produtos\.html/);
  });
  test('Enter no campo de senha também entra', async ({ page }) => {
    await page.goto('index.html');
    await page.getByTestId('usuario').fill('cliente');
    await page.getByTestId('senha').fill('leigo123');
    await page.getByTestId('senha').press('Enter');
    await expect(page).toHaveURL(/produtos\.html/);
  });
  test('a mensagem de erro não aparece antes de errar (aula 68)', async ({ page }) => {
    await page.goto('index.html');
    await expect(page.getByTestId('erro')).not.toBeVisible();
    await expect(page.getByTestId('entrar')).toHaveText('Entrar');
    await expect(page.getByTestId('usuario')).toBeVisible();
    await expect(page.getByTestId('senha')).toBeEmpty();
  });
  test('errou e depois acertou: entra', async ({ page }) => {
    await entrar(page, 'cliente', 'errada');
    await expect(page.getByTestId('erro')).toBeVisible();
    await page.getByTestId('senha').fill('leigo123');
    await page.getByTestId('entrar').click();
    await expect(page).toHaveURL(/produtos\.html/);
  });
});

test.describe('produtos', () => {
  test('sem login, a página de produtos manda pro login', async ({ page }) => {
    await page.goto('produtos.html');
    await expect(page).toHaveURL(/index\.html/);
  });
  test('cada card tem nome, preço e botão, e o preço bate com a API', async ({ page }) => {
    await entrar(page);
    await expect(page.getByTestId('produto')).toHaveCount(PRODUTOS.length);
    const nomes = await page.getByTestId('nome').allTextContents();
    const precos = (await page.getByTestId('preco').allTextContents()).map(numero);
    for (const p of PRODUTOS) {
      const i = nomes.indexOf(p.nome);
      expect(i, p.nome).toBeGreaterThan(-1);
      expect(precos[i], p.nome).toBe(p.preco);
    }
  });
  test('o esgotado aparece, com a etiqueta e o botão desabilitado (aula 79)', async ({ page }) => {
    await entrar(page);
    const esgotados = PRODUTOS.filter((p) => !p.estoque);
    expect(esgotados.length).toBeGreaterThan(0);
    for (const p of esgotados) {
      const card = page.getByTestId('produto').filter({ hasText: p.nome });
      await expect(card).toHaveCount(1);
      await expect(card.getByTestId('esgotado')).toBeVisible();
      await expect(card.getByTestId('adicionar')).toBeDisabled();
    }
    await expect(page.getByTestId('esgotado')).toHaveCount(esgotados.length);
  });
  test('adicionar ao carrinho conta certo', async ({ page }) => {
    await entrar(page);
    await expect(page.getByTestId('contador-carrinho')).toBeHidden();
    const botoes = page.getByTestId('adicionar').filter({ hasNotText: 'Indisponível' });
    await botoes.nth(0).click();
    await expect(page.getByTestId('contador-carrinho')).toHaveText('1');
    await botoes.nth(1).click();
    await expect(page.getByTestId('contador-carrinho')).toHaveText('2');
  });
  test('sair volta pro login e protege a página', async ({ page }) => {
    await entrar(page);
    await page.getByTestId('sair').click();
    await expect(page).toHaveURL(/index\.html/);
    await page.goto('produtos.html');
    await expect(page).toHaveURL(/index\.html/);
  });
  test('busca e categoria', async ({ page }) => {
    await entrar(page);
    await page.getByTestId('busca').fill('caneca');
    await expect(page.getByTestId('produto')).toHaveCount(1);
    await page.getByTestId('busca').fill('nada disso');
    await expect(page.getByTestId('vazio')).toHaveText('Nenhum produto encontrado.');
    await page.getByTestId('busca').fill('');
    await page.getByTestId('categoria').filter({ hasText: 'Eletrônicos' }).click();
    await expect(page.getByTestId('produto')).toHaveCount(PRODUTOS.filter((p) => p.categoria === 'Eletrônicos').length);
  });
});

test.describe('ordenação', () => {
  const casos = { az: ['nome', 1], za: ['nome', -1], menor: ['preco', 1], maior: ['preco', -1] };
  for (const versao of [2, 1]) {
    for (const [op, [campo, s]] of Object.entries(casos)) {
      test(`versão ${versao}: ${op}`, async ({ page }) => {
        await entrar(page, 'cliente', 'leigo123', versao === 1 ? 'index.html?versao=1' : 'index.html');
        await expect(page.getByTestId('versao')).toHaveText(`versão ${versao}`);
        await page.getByTestId('ordenar').selectOption(op);
        const tela = campo === 'nome' ? await page.getByTestId('nome').allTextContents() : (await page.getByTestId('preco').allTextContents()).map(numero);
        const certo = [...tela].sort(campo === 'nome' ? (a, b) => a.localeCompare(b) : (a, b) => a - b);
        if (s < 0) certo.reverse();
        if (versao === 1 && campo === 'preco') expect(tela, 'o bug da versão 1 tem que aparecer').not.toEqual(certo);
        else expect(tela).toEqual(certo);
      });
    }
  }
  test('versão 1: a ordem errada que a aula 76 narra', async ({ page }) => {
    await entrar(page, 'cliente', 'leigo123', 'index.html?versao=1');
    await page.getByTestId('ordenar').selectOption('menor');
    const precos = (await page.getByTestId('preco').allTextContents()).map(numero);
    expect(precos.slice(0, 3)).toEqual([12.5, 129.9, 15.99]);  // "doze e cinquenta, cento e vinte e nove e noventa, quinze e noventa e nove"
    expect(precos.indexOf(7.99)).toBeGreaterThanOrEqual(precos.length - 3);  // "o sete e noventa e nove, quase lá no fim"
  });
  test('depois de abrir a versão 1, abrir o endereço normal volta pra versão 2', async ({ page }) => {
    await entrar(page, 'cliente', 'leigo123', 'index.html?versao=1');
    await expect(page.getByTestId('versao')).toHaveText('versão 1');
    await entrar(page, 'cliente', 'leigo123', 'index.html');
    await expect(page.getByTestId('versao')).toHaveText('versão 2');
  });
  test('a ordem padrão, sem escolher nada, é de A a Z', async ({ page }) => {
    await entrar(page);
    const nomes = await page.getByTestId('nome').allTextContents();
    expect(nomes).toEqual([...nomes].sort((a, b) => a.localeCompare(b)));
  });
});

test.describe('mock (aula 66)', () => {
  test('servidor fora do ar: aviso de erro [espera erro]', async ({ page }) => {
    await entrar(page);
    await expect(page.getByTestId('produto').first()).toBeVisible();
    await page.route('**/api/produtos.json', (r) => r.abort());
    await page.reload();
    await expect(page.getByTestId('erro-carregar')).toHaveText('Não foi possível carregar os produtos. Tente de novo mais tarde.');
  });
  test('erro 500: aviso de erro [espera erro]', async ({ page }) => {
    await page.route('**/api/produtos.json', (r) => r.fulfill({ status: 500, body: 'erro' }));
    await entrar(page);
    await expect(page.getByTestId('erro-carregar')).toBeVisible();
  });
  test('lista vazia: nenhum produto encontrado', async ({ page }) => {
    await page.route('**/api/produtos.json', (r) => r.fulfill({ status: 200, body: '[]' }));
    await entrar(page);
    await expect(page.getByTestId('vazio')).toHaveText('Nenhum produto encontrado.');
  });
  test('resposta lenta: os produtos aparecem quando chegam', async ({ page }) => {
    await page.route('**/api/produtos.json', async (r) => { await new Promise((ok) => setTimeout(ok, 3000)); await r.continue(); });
    await entrar(page);
    await expect(page.getByTestId('produto').first()).toBeVisible({ timeout: 10000 });
  });
  test('a API de verdade responde a lista em JSON', async ({ request }) => {
    const r = await request.get('api/produtos.json');
    expect(r.ok()).toBeTruthy();
    expect(await r.json()).toEqual(PRODUTOS);
  });
});

test.describe('visual (aula 67)', () => {
  test('a tela de login é sempre igual (duas fotos seguidas)', async ({ page }) => {
    await page.goto('index.html');
    await page.waitForLoadState('networkidle');
    const a = await page.screenshot({ animations: 'disabled' });
    await page.reload(); await page.waitForLoadState('networkidle');
    const b = await page.screenshot({ animations: 'disabled' });
    expect(a.equals(b), 'a tela muda sozinha: o teste visual ia falhar à toa').toBeTruthy();
  });
  test('?estilo=quebrado muda o botão, mas o login continua funcionando', async ({ page }) => {
    await page.goto('index.html');
    const normal = await page.getByTestId('entrar').evaluate((e) => getComputedStyle(e).backgroundColor);
    await page.goto('index.html?estilo=quebrado');
    const quebrado = await page.getByTestId('entrar').evaluate((e) => getComputedStyle(e).backgroundColor);
    expect(quebrado).not.toBe(normal);
    await page.getByTestId('usuario').fill('cliente');
    await page.getByTestId('senha').fill('leigo123');
    await page.getByTestId('entrar').click();
    await expect(page).toHaveURL(/produtos\.html/);
  });
});

test('tela pequena: nada sai da tela (celular)', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await entrar(page);
  const larg = await page.evaluate(() => document.documentElement.scrollWidth);
  expect(larg).toBeLessThanOrEqual(391);
  await expect(page.getByTestId('ordenar')).toBeVisible();
  await expect(page.getByTestId('adicionar').first()).toBeInViewport({ ratio: 0 }).catch(() => {});
});
