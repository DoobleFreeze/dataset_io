<script>
    import { onMount } from "svelte";
    import {browser} from '$app/environment';

	const urlAuth = "https://dataset-io.onrender.com/api/check/";
	export let code_response;
    let user_session;
    if (browser){
        console.log(localStorage.getItem('token'));
        user_session = localStorage.getItem('token');
    }
    export let user_id;

    onMount(async function () {
        const isAuth = await fetch(urlAuth+user_session);
        const dataAuth = await isAuth.json();
        console.log(dataAuth);
        code_response = dataAuth["response_code"];
        user_id = dataAuth["data"];

        if (code_response == 400) {
            window.location.href = '/login';
        }
    });

    async function logout () {
        const res = await fetch('https://dataset-io.onrender.com/api/logout', {
        
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_session
            })
        })
    
        const json = await res.json()
        console.log(json)
        let result = json['response_code']
        console.log(result)
        if (result == 200) {
            window.location.href = '/main';
        }
	}
</script>

<main>
    <!--**********************************
        Main wrapper start
    ***********************************-->
    <div id="main-wrapper">
        <!--**********************************
            Nav header start
        ***********************************-->
        <div class="nav-header">
            <div class="brand-logo">
                <a href="/main">
                    <b class="logo-abbr"><img src="images/logo.png" alt=""> </b>
                    <span class="logo-compact"><img src="./images/logo-compact.png" alt=""></span>
                    <span class="brand-title">
                        <!-- <img src="images/logo-text.png" alt=""> -->
                        <h3 style="color:white">Dataset IO</h3>
                    </span>
                </a>
            </div>
        </div>
        <!--**********************************
            Nav header end
        ***********************************-->

        <!--**********************************
            Header start
        ***********************************-->
        <div class="header">    
            <div class="header-content clearfix">
                
                <!-- <div class="nav-control">
                    <div class="hamburger">
                        <span class="toggle-icon"><i class="icon-menu"></i></span>
                    </div>
                </div> -->
                <!-- <div class="header-left">
                    <div class="input-group icons">
                        <div class="input-group-prepend">
                            <span class="input-group-text bg-transparent border-0 pr-2 pr-sm-3" id="basic-addon1"><i class="mdi mdi-magnify"></i></span>
                        </div>
                        <input type="search" class="form-control" placeholder="Search Dashboard" aria-label="Search Dashboard">
                        <div class="drop-down animated flipInX d-md-none">
                            <form action="#">
                                <input type="text" class="form-control" placeholder="Search">
                            </form>
                        </div>
                    </div>
                </div> -->
                <div class="header-right">
                    <ul class="clearfix">
                        <li class="icons dropdown">
                            {#if code_response == 200}
                            <div class="user-img c-pointer position-relative"   data-toggle="dropdown">
                                <!-- <img src="images/user/1.png" height="40" width="40" alt=""> -->
                                <img src="./images/avatar/user.png" height="40" width="40" alt="">
                            </div>
                            <div class="drop-down dropdown-profile animated fadeIn dropdown-menu">
                                <div class="dropdown-content-body">
                                    <ul>
                                        <li>
                                            <a href="/profile"><i class="icon-user"></i> <span>Profile</span></a>
                                        </li>
                                        
                                        <hr class="my-2">
                                        <li>
                                            <button on:click={logout} style="border: none; background-color: white">
                                                <a href="/main"><i class="icon-key"></i> <span >Logout</span></a>
                                            </button>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            {:else}
                            <div class="dropdown">
                                <a href="/login" class="header-a-right">
                                    <span class="right-header">Войти</span>
                                </a>
                            </div>
                            {/if}
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <!--**********************************
            Header end ti-comment-alt
        ***********************************-->

         <!--**********************************
            Sidebar start
        ***********************************-->
        <div class="nk-sidebar">           
            <div class="nk-nav-scroll">
                <ul class="metismenu" id="menu">
                    <li class="nav-label"><a href="/dashboard">Общий Dashboard</a></li>
                    <li class="nav-label"><a href="/mydashboard">Личный Dashboard</a></li>
                    <li class="nav-label"><a href="/datasets">Датасеты</a></li>
                    <li class="nav-label"><a href="/upload">Загрузка Датасета</a></li>
                </ul>
            </div>
        </div>
        <!--**********************************
            Sidebar end
        ***********************************-->

        <slot/>

        <!--**********************************
            Footer start
        ***********************************-->
        <div class="footer">
            <div class="copyright">
                <p>Nikita</p>
            </div>
        </div>
        <!--**********************************
            Footer end
        ***********************************-->
    </div>
    <!--**********************************
        Main wrapper end
    ***********************************-->

    <script src="plugins/common/common.min.js"></script>
    <script src="js/custom.min.js"></script>
    <script src="js/settings.js"></script>
    <script src="js/gleek.js"></script>
    <script src="js/styleSwitcher.js"></script>

     <!-- Chartjs -->
    <script src="./plugins/chart.js/Chart.bundle.min.js"></script>
    <!-- Circle progress -->
    <script src="./plugins/circle-progress/circle-progress.min.js"></script>
    <!-- Datamap -->
    <script src="./plugins/d3v3/index.js"></script>
    <script src="./plugins/topojson/topojson.min.js"></script>
    <script src="./plugins/datamaps/datamaps.world.min.js"></script>
    <!-- Morrisjs -->
    <script src="./plugins/raphael/raphael.min.js"></script>
    <script src="./plugins/morris/morris.min.js"></script>
    <!-- Pignose Calender -->
    <script src="./plugins/moment/moment.min.js"></script>
    <script src="./plugins/pg-calendar/js/pignose.calendar.min.js"></script>
    <!-- ChartistJS -->
    <script src="./plugins/chartist/js/chartist.min.js"></script>
    <script src="./plugins/chartist-plugin-tooltips/js/chartist-plugin-tooltip.min.js"></script>



    <script src="./js/dashboard/dashboard-1.js"></script>
</main>