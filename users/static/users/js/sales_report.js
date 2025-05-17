document.addEventListener("DOMContentLoaded", function () {
  
    const canvas = document.getElementById("salesChart");
    const shopID = canvas?.dataset.shopId;  
  
    if (!shopID) {
      console.warn("Shop ID not found. Chart will not render.");
      return;
    }
  
    fetch(`/api/sales-summary/${shopID}/`)
      .then(response => response.json())
      .then(data => {
        const labels = data.map(item => item.product_name);
        const revenues = data.map(item => parseFloat(item.total_revenue));
  
        const ctx = canvas.getContext("2d");
        new Chart(ctx, {
          type: "bar",
          data: {
            labels: labels,
            datasets: [{
              label: "Revenue (Ksh)",
              data: revenues,
              backgroundColor: "rgba(54, 162, 235, 0.6)",
              borderColor: "rgba(54, 162, 235, 1)",
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      })
      .catch(err => {
        console.error("Error loading chart data:", err);
      });
  });
  