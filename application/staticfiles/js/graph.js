function create_graph(stats, id, title) {
  const ctx = document.getElementById(id);
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
