async function carregarIndicadores() {
  const token = localStorage.getItem("access_token");
  if (!token) {
    window.location.href = "/login";
    return;
  }

  const codigoIbge = "2611606"; // padrão demo
  try {
    const resp = await fetch(`/api/v1/indicadores/${codigoIbge}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (!resp.ok) {
      throw new Error("Falha ao carregar indicadores");
    }
    const data = await resp.json();
    preencherCards(data);
    montarGrafico(data);
  } catch (err) {
    console.error(err);
  }
}

function preencherCards(indicadores) {
  const total = indicadores.length;
  const atingiram = indicadores.filter((i) => i.atingiu_meta === true).length;
  const abaixo = total - atingiram;

  document.getElementById("card-indicadores-atingidos").textContent = atingiram;
  document.getElementById("card-indicadores-abaixo").textContent = abaixo;

  // Placeholder para cadastros/atendimentos se disponíveis futuramente
  document.getElementById("card-total-cadastros").textContent = "--";
  document.getElementById("card-total-atendimentos").textContent = "--";
}

function montarGrafico(indicadores) {
  const ctx = document.getElementById("chartIndicadores");
  if (!ctx) return;
  const labels = indicadores.map((i) => `${i.indicador} (${i.periodo_referencia})`);
  const valores = indicadores.map((i) => Number(i.valor ?? 0));

  new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Valor do indicador",
          data: valores,
          backgroundColor: "rgba(13,110,253,0.6)",
          borderColor: "rgba(13,110,253,1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true },
      },
    },
  });
}

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("chartIndicadores")) {
    carregarIndicadores();
  }
});
