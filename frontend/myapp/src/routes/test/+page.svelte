

<script>
    import { onMount } from 'svelte';
    import { Line } from 'svelte-chartjs'

    let portfolio;
    const data = {
          labels: ['Expenses', 'Savings', 'Investments'],
          datasets: [
              {
                  label: 'My First Dataset',
                  data: [300, 50, 100],
                  backgroundColor: ['#7000e1', '#fc8800', '#00b0e8'],
                  // hoverOffset: 4,
                  borderWidth: 0
              }
          ]
      };
      const config = {
          type: 'bar',
          data: data,
          options: {
              borderRadius: '30',
              responsive: true,
              cutout: '95%',
              spacing: 2,
              plugins: {
                  legend: {
                      position: 'bottom',
                      display: true,
                      labels: {
                          usePointStyle: true,
                          padding: 20,
                          font: {
                              size: 14
                          }
                      }
                  },
                  title: {
                      display: true,
                      text: 'My Personal Portfolio'
                  }
              }
          }
      };
    onMount(()=> {
      const ctx = portfolio.getContext('2d');
      // Initialize chart using default config set
      var myChart = new Chart(ctx, config);
    })
  </script>

<canvas bind:this={portfolio} width={100} height={100} />




<div class="col-lg-3 col-md-6">
    <div class="card card-widget">
        <div class="card-body">
            <h5>Статистика </h5>
            <div class="mt-4">
                <h6>Занято памяти <span class="pull-right">30%</span></h6>
            </div>
            <div class="mt-4">
                <h6>Количество датасетов <span class="pull-right">5</span></h6>
            </div>
            <div class="mt-4">
                <h6>Количество скачанных датасетов <span class="pull-right">20%</span></h6>
            </div>
            <div class="mt-4">
                <h6>Количество пользователей <span class="pull-right">5</span></h6>
            </div>
        </div>
    </div>
</div>