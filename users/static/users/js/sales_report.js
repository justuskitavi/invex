document.addEventListener("DOMContentLoaded", function () {
    const shopID = document.getElementById("generalSalesChart").dataset.shopId;
  
    if (!shopID) {
      console.warn("Shop ID not found. Charts will not render.");
      return;
    }
  
    // Function to create a chart
    function createBarChart(ctx, labels, data, label) {
      return new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [{
            label: label,
            data: data,
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
    }
  
    // Load general sales data
    fetch(`/api/sales-summary/${shopID}/`)
      .then(response => response.json())
      .then(data => {
        const labels = data.map(item => item.product_name);
        const revenues = data.map(item => parseFloat(item.total_revenue));
  
        const ctx = document.getElementById("generalSalesChart").getContext("2d");
        createBarChart(ctx, labels, revenues, "Revenue (Ksh)");
      })
      .catch(err => {
        console.error("Error loading general sales data:", err);
      });
  
    // Load individual product sales data
    document.querySelectorAll('.product-chart').forEach(canvas => {
      const productID = canvas.dataset.productId;
      const ctx = canvas.getContext('2d');
  
      // Fetch sales data for each product
      fetch(`/api/product-sales/?productID=${productID}&months=12`) // Adjust months if needed
        .then(response => response.json())
        .then(data => {
          const labels = data.map(item => new Date(item.month).toLocaleString('default', { month: 'short', year: 'numeric' }));
          const revenues = data.map(item => parseFloat(item.total_revenue));
          createBarChart(ctx, labels, revenues, `Sales for Product ID: ${productID}`);
        })
        .catch(err => {
          console.error(`Error loading sales data for product ${productID}:`, err);
        });
    });
  });