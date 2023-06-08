<script>
    // let datasets = [
    //     {name: "Преступление и наказание", updoad_time: "24.04.2023", man: "Геннадий Головкин"},
    //     {name: "Фильмы и мультфильмы", updoad_time: "22.04.2023", man: "Осипов Никита"},
    //     {name: "Мстители", updoad_time: "18.04.2023", man: "Осипов Никита"},
    //     {name: "Бархатные тяги", updoad_time: "18.04.2023", man: "Осипов Никита"},
    //     {name: "Диски нормальные", updoad_time: "14.12.2023", man: "Виталий Парамонов"},
    //     {name: "Кефтеме", updoad_time: "07.04.2023", man: "Авгян Пасенян"},
    // ]

    import { onMount } from "svelte";
    import {browser} from '$app/environment';

    const urlAuth = "https://dataset-io.onrender.com/api/check/";
    let user_session;
    if (browser){
        user_session = localStorage.getItem('token');
    }
    let user_id;
    let code_response;
    export let datasets = [];
     onMount(async function () {
        const isAuth = await fetch(urlAuth+user_session);
        const dataAuth = await isAuth.json();
        console.log(dataAuth);
        code_response = dataAuth["response_code"];
        user_id = dataAuth["data"];

        const get_datasets = await fetch("https://dataset-io.onrender.com/api/get_datasets");
        const datasets_json = await get_datasets.json();
        console.log(datasets_json);
        datasets = datasets_json["data"]["datasets"];
    });
    
    async function get_dataset (dataset_id) {
        const res = await fetch('https://dataset-io.onrender.com/api/get_dataset/' + dataset_id + "/" + user_id, {
            mode: 'no-cors',
            method: 'GET',
        headers: {
            'Content-Type': 'application/x-zip-compressed'
        },
        // body: JSON.stringify({
        //     login,
        //     email,
        //     password,
        //     second_password
        // })
    })

    const json = await res.blob();
    console.log(json)

    const url = window.URL.createObjectURL(json);
        const a = document.createElement("a");
        a.style.display = "none";
        a.href = url;
        // the filename you want
        a.download = "dataset.zip";
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        // alert("your file has downloaded!");

}

    async function download (dataset_id){
        window.location.href = "https://dataset-io.onrender.com/api/get_dataset/" + dataset_id + "/" + user_id;
    }

    async function delete_dataset (dataset_id){
        const res = await fetch('https://dataset-io.onrender.com/api/delete_dataset/' + dataset_id, {
            mode: 'no-cors',
            method: 'GET',
        });
        window.location.href = "/datasets";
    }
</script>

<main>
     <!--**********************************
            Content body start
        ***********************************-->
        <div class="content-body">
            <div class="row">
                {#each datasets as dataset}
                <div class="col-lg-12 block1">
                    
                    <div class="row ">
                        <div class="col-md-8 col-sm-8 col-8">
                            <h2>{dataset.name}</h2>
                        </div>
                        <div class="col-md-4 col-sm-4 col-4 text-right">
                             <!-- <a href="/static/models/fake_model_images/tasks/1" class="btn btn-ch-dl" title="Скачать">Удалить</a> -->
                            <button class="btn btn-ch-dl" on:click={delete_dataset(dataset.ds_id)}>Удалить</button>
                            <button class="btn btn-ch-dl" on:click={download(dataset.ds_id)}>Загрузить</button>
                        </div>
                    </div>
                    <div class="text-main pb-2">
                        <font color="#808080">Дата загрузки: </font>
                        {dataset.date_load}
                    </div>
                    <!-- <div class="pb-10">
                        <font color="#808080"></font>
                        <a href="/" class="a-profile">man</a>
                    </div> -->
                    
                </div>
                {/each}
            </div>
        </div>
        <!--**********************************
            Content body end
        ***********************************-->
</main>

<style>
    .block1 {
        padding: 1rem;
        width: 420px;
        box-shadow: 0 15px 30px 0 rgba(0,0,0,0.11),
            0 5px 15px 0 rgba(0,0,0,0.08);
        background-color: #ffffff;
        border-radius: 0.5rem;
        
        border-left: 0 solid #00ff99;
        transition: border-left 300ms ease-in-out, padding-left 300ms ease-in-out;
        padding-left: 50px;

    }
</style>