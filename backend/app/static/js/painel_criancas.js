async function carregarPainelCriancas() {
  const token = localStorage.getItem("access_token");
  if (!token) {
    window.location.href = "/login";
    return;
  }
  const codigoIbge = "2611606"; // demo
  try {
    const resp = await fetch(`/api/v1/painel/criancas/${codigoIbge}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!resp.ok) throw new Error("Falha ao carregar painel de crianças");
    const data = await resp.json();
    preencherCriancasResumo(data);
    preencherCriancasTabela(data);
  } catch (err) {
    console.error(err);
  }
}

function preencherCriancasResumo(data) {
  const total = data.length;
  const hoje = new Date();
  const ultimo30 = data.filter((c) => diffDias(c.data_ultimo_atendimento, hoje) <= 30).length;
  const faixas = {};
  data.forEach((c) => {
    const f = c.faixa_etaria || "N/A";
    faixas[f] = (faixas[f] || 0) + 1;
  });
  const distrib = Object.entries(faixas)
    .map(([faixa, qtd]) => `${faixa}: ${qtd}`)
    .join(" | ");

  document.getElementById("cri-total").textContent = total;
  document.getElementById("cri-30d").textContent = ultimo30;
  document.getElementById("cri-faixas").textContent = distrib || "--";
}

function preencherCriancasTabela(data) {
  const tbody = document.getElementById("criancas-tbody");
  tbody.innerHTML = "";
  data.forEach((c) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${c.hash_identificador ?? "-"}</td>
      <td>${c.unidade ?? "-"}</td>
      <td>${c.equipe ?? "-"}</td>
      <td>${c.faixa_etaria ?? "-"}</td>
      <td>${c.qtd_atendimentos_12m ?? 0}</td>
      <td>${c.data_ultimo_atendimento ?? "-"}</td>
    `;
    tbody.appendChild(tr);
  });
}

function diffDias(dataIso, hoje) {
  if (!dataIso) return Number.POSITIVE_INFINITY;
  const dt = new Date(dataIso);
  const diffMs = hoje - dt;
  return Math.floor(diffMs / (1000 * 60 * 60 * 24));
}

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("criancas-tbody")) {
    carregarPainelCriancas();
  }
});
