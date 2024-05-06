function create_graph(baseStats, id, title) {
  const ctx = document.getElementById(id);
  const stats = baseStats[id];
  console.log(stats)
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: stats.labels,
      datasets: stats.datasets,
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          stacked: true,
        },
        y: {
          stacked: true
        }
      },
      plugins: {
        title: {
          display: true,
          text: title
        },
      },
    },
  });
}
