<script>
    import { onMount } from 'svelte';
    import {browser} from '$app/environment';
    import { Line } from 'svelte-chartjs';

    const urlAuth = "https://dataset-io.onrender.com/api/check/";
    let user_session;
    if (browser){
        user_session = localStorage.getItem('token');
    }
    let user_id;
    let code_response;

    export let panels = [];
    let portfolio;
    export let activity = [];
    export let users_anal = [];
    export let graf = [];
    onMount(async function () {
        const isAuth = await fetch(urlAuth+user_session);
        const dataAuth = await isAuth.json();
        console.log(dataAuth);
        code_response = dataAuth["response_code"];
        user_id = dataAuth["data"];

        const user_dash = await fetch("https://dataset-io.onrender.com/api/get_user_dashboard/" + user_id);
        const dash_json = await user_dash.json();
        console.log(dash_json);
        panels = dash_json["data"]["panels"];
        console.log(panels);

        graf = dash_json["data"]["graf"];

        activity = dash_json["data"]["last_activity"];

        users_anal = dash_json["data"]["users_anal"];

        const config = {
          type: 'bar',
          data: graf,
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

      
        
      console.log(graf);
      const ctx = portfolio.getContext('2d');
      // Initialize chart using default config set
      var myChart = new Chart(ctx, config);
    });
  </script>

<main>
    <div class="content-body">
        <div class="container-fluid mt-3">
            <div class="row">
                <div class="col-lg-3 col-sm-6">
                    <div class="card gradient-1">
                        <div class="card-body">
                            <h3 class="card-title text-white">Занято памяти</h3>
                            <div class="d-inline-block">
                                <h2 class="text-white">{panels.all_memory}</h2>
                            </div>
                            <span class="float-right display-5 opacity-5"></span>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-sm-6">
                    <div class="card gradient-2">
                        <div class="card-body">
                            <h3 class="card-title text-white">Датасеты</h3>
                            <div class="d-inline-block">
                                <h2 class="text-white">{panels.count_ds}</h2>
                            </div>
                            <span class="float-right display-5 opacity-5"></span>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-sm-6">
                    <div class="card gradient-3">
                        <div class="card-body">
                            <h3 class="card-title text-white">Скачанные Датасеты</h3>
                            <div class="d-inline-block">
                                <h2 class="text-white">{panels.count_download}</h2>
                            </div>
                            <span class="float-right display-5 opacity-5"></span>
                        </div>
                    </div>
                </div>
                <div class="col-lg-3 col-sm-6">
                    <div class="card gradient-4">
                        <div class="card-body">
                            <h3 class="card-title text-white">Действий на сайте</h3>
                            <div class="d-inline-block">
                                <h2 class="text-white">{panels.count_history}</h2>
                            </div>
                            <span class="float-right display-5 opacity-5"></span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-lg-6 col-md-12">
                    <div class="card">
                        <div class="card-body">
                            <h4 class="card-title">График</h4>
                            <!-- <canvas id="myChart"></canvas> -->
                            <div class="mychart"><canvas bind:this={portfolio} width={150} height={100} /></div>
                            
                        </div>
                    </div>
                </div>    


                <div class="col-xl-6 col-lg-6 col-sm-6 col-xxl-6">
                    <div class="card">
                        <div class="card-body">
                            <h4 class="card-title">Последняя активность</h4>
                            <div id="activity">
                                <div id="activity">
                                    {#each activity as activ}
                                    <div class="media border-bottom-1 pt-3 pb-3">
                                        <img width="35" src="./images/avatar/user.png" class="mr-3 rounded-circle">
                                        <div class="media-body">
                                            <h5>{activ.nickname}</h5>
                                            <p class="mb-0">{activ.text_label}</p>
                                        </div><span class="text-muted ">{activ.data_label}</span>
                                    </div>
                                    {/each}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- <script src="./js/mychart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script> -->
</main>

<style>
    #activity {
        overflow-y: scroll;
        height: 340px;
    }
</style>