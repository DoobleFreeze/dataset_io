<script>
      import { onMount } from "svelte";
    import {browser} from '$app/environment';

    const urlAuth = "https://dataset-io.onrender.com/api/check/";
    let user_session;
    if (browser){
        user_session = localStorage.getItem('token');
    }
    let user_id;
    let code_response;
     onMount(async function () {
        const isAuth = await fetch(urlAuth+user_session);
        const dataAuth = await isAuth.json();
        console.log(dataAuth);
        code_response = dataAuth["response_code"];
        user_id = dataAuth["data"];
    });

    let data;
    let namefile;

    async function upload () {
        var input = document.querySelector('input[type="file"]')
        console.log(data)
        let fdata = new FormData()
        // fdata.append('dataset', data)
        fdata.append('dataset', input.files[0])
        const res = await fetch('https://dataset-io.onrender.com/api/add_dataset/' + user_id + '/' + namefile, {
            mode: 'no-cors',
            method: 'POST',
            // headers: {
            //     'Content-Type': 'multipart/form-data'
            // },
            // body: JSON.stringify({
            //     "dataset": data
			// })
            body: fdata
        })
    
        // const json = await res.json()
        // console.log(json)
        // result = json['response_code']
        // console.log(result)
	}
</script>

<main>
    <!--**********************************
            Content body start
        ***********************************-->
        <div class="content-body">
            <div class="row">
                <div class="col-lg-12 block1">
                    <h2>Загрузка датасета</h2>
                    <form>
                    <div class="col-6 mb-3">
                        <input type="file" id="file-uploader" bind:value={data} class="upload">
                    </div>
                    
                    <div class="col-6">
                        <div class="card card-profile text-center">
                            <input type="text" id ="username" bind:value={namefile} name = "username" placeholder="namefile" autofocus="autofocus">
                        </div>
                    </div>

                    <div class="col-12">
                        <button class="btn btn-danger px-5" on:click={upload}>Отправить</button>
                    </div>
                </form>
                </div>
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
        padding-top: 10px;

        height: 500px;
    }

    .upload {
        margin-top: 30px;
    }
</style>