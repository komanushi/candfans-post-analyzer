function create_graph(id, title) {
  const ctx = document.getElementById(id);
  const stats = summaryMonthlyStats[id];
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
