async function carregarPainelGestantes() {
  const token = localStorage.getItem("access_token");
  if (!token) {
    window.location.href = "/login";
    return;
  }
  const codigoIbge = "2611606"; // demo
  try {
    const resp = await fetch(`/api/v1/painel/gestantes/${codigoIbge}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!resp.ok) throw new Error("Falha ao carregar painel de gestantes");
    const data = await resp.json();
    preencherGestantesResumo(data);
    preencherGestantesTabela(data);
  } catch (err) {
    console.error(err);
  }
}

function preencherGestantesResumo(data) {
  const total = data.length;
  const hoje = new Date();
  const ultimo30 = data.filter((g) => diffDias(g.data_ultimo_atendimento, hoje) <= 30).length;
  const sem90 = data.filter((g) => diffDias(g.data_ultimo_atendimento, hoje) > 90).length;

  document.getElementById("gest-total").textContent = total;
  document.getElementById("gest-30d").textContent = ultimo30;
  document.getElementById("gest-90d").textContent = sem90;
}

function preencherGestantesTabela(data) {
  const tbody = document.getElementById("gestantes-tbody");
  tbody.innerHTML = "";
  data.forEach((g) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${g.hash_identificador ?? "-"}</td>
      <td>${g.unidade ?? "-"}</td>
      <td>${g.equipe ?? "-"}</td>
      <td>${g.faixa_etaria ?? "-"}</td>
      <td>${g.qtd_atendimentos_12m ?? 0}</td>
      <td>${g.data_ultimo_atendimento ?? "-"}</td>
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
  if (document.getElementById("gestantes-tbody")) {
    carregarPainelGestantes();
  }
});
