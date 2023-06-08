<main><!--**********************************
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
            </div>
        </div>
        <!--**********************************
            Header end ti-comment-alt
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
</main>

<style>
    .header {
        background-color: #111B27;
    }

    .footer {
        background-color: #111B27;
    }

    .copyright {
        background-color: #111B27;
        margin-left: -200px;
    }
</style>
