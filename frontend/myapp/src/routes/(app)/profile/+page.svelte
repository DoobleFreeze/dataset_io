<script>
    import { onMount } from "svelte";
    import {browser} from '$app/environment';

    const url = "https://dataset-io.onrender.com/api/get_profile/";
    const urlAuth = "https://dataset-io.onrender.com/api/check/";
	export let code_response;
    let user_session;
    if (browser){
        user_session = localStorage.getItem('token');
    }
    let user_id;
    export let user_info;

    export let email;
    export let nickname;
    export let image_path;
    let password;
    export let result;

    export let user_activity = [];

    let new_login;
    let new_password;
    let old_password;
    let new_second_password;
    let new_image_path;

    onMount(async function () {
        const isAuth = await fetch(urlAuth+user_session);
        const dataAuth = await isAuth.json();
        console.log(dataAuth);
        code_response = dataAuth["response_code"];
        user_id = dataAuth["data"];
        
        
        const response = await fetch(url+user_id);
        const data = await response.json();
        console.log(data);
        user_info = data["data"]["user_info"];
        email = user_info["email"];
        nickname = user_info["login"];
        password = user_info["password"];
        image_path = user_info["image_path"];

        user_activity = data["data"]["user_activity"];
        console.log(user_activity);
    });


    async function update_user () {
        if (new_login != "" && new_password != "" && old_password != "" && new_second_password != "") {
            const res = await fetch('https://dataset-io.onrender.com/api/update_user/' + user_id, {
            
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    "login": new_login,
                    "password": new_password,
                    "image_path": image_path
                })
		    })
		
            const json = await res.json()
            console.log(json)
            result = json['response_code']
            console.log(result)
        }
		else {
            result = 401
        }
	} 
</script>

<main>
        <!--**********************************
            Content body start
        ***********************************-->
        <div class="content-body">
            {#if result == 401}
            <div>
                <div class="alert alert-danger">Заполните все поля!</div>
            </div>
            {/if}

            <div class="container-fluid">
                <div class="row">
                    <div class="col-lg-6 col-xl-6">
                        <div class="card">
                            <div class="card-body ah">
                                <div class="media align-items-center mb-4">
                                    <img class="mr-3" src="./images/avatar/user.png" width="80" height="80" alt="">
                                    <div class="media-body">
                                        <h3 class="mb-0">{nickname}</h3>
                                    </div>
                                </div>
                                <form>
                                    <div class="row mb-5">
                                    
                                        <div class="col-6">
                                            <div class="card card-profile text-center">
                                                <input type="text" name = "username" bind:value={new_login} placeholder="nickname" autofocus="autofocus">
                                            </div>
                                        </div>
                                        <div class="col-6">
                                            <div class="card card-profile text-center">
                                                <input type="password" name = "username" bind:value={old_password} placeholder="old password" autofocus="autofocus">
                                            </div>
                                        </div>
                                        <div class="col-6">
                                            <div class="card card-profile text-center">
                                                <input type="password" name = "username" bind:value={new_password} placeholder="new password" autofocus="autofocus">
                                            </div>
                                        </div>
                                        <div class="col-6">
                                            <div class="card card-profile text-center">
                                                <input type="password" name = "username" bind:value={new_second_password} placeholder="matching password" autofocus="autofocus">
                                            </div>
                                        </div>
                                        
                                    <div class="col-12 text-center">
                                        <button class="btn btn-danger px-5" on:click={update_user}>Подтвердить изменения</button>
                                    </div>
                                </div>
                                </form>
                                <ul class="card-profile__info">
                                    <li><strong class="text-dark mr-4">Email</strong> <span>{email}</span></li>
                                </ul>
                            </div>
                        </div>  
                    </div>

                    <div class="col-xl-6 col-lg-6 col-sm-6 col-xxl-6">
                        <div class="card">
                            <div class="card-body">
                                <h4 class="card-title">Последняя активность</h4>
                                <div id="activity">
                                    <div id="activity">
                                        {#each user_activity as activ}
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
            <!-- #/ container -->
        </div>
        <!--**********************************
            Content body end
        ***********************************-->
</main>

<style>
    input {
    width: 100%;
    height: 100%;
    outline: none;
    padding: 0 45px;
    font-size: 18px;
    background: none;
    caret-color: black;
    border-radius: 5px;
    border: 1px solid #bfbfbf;
    border-bottom-width: 2px;
    transition: all 0.2s ease;
}

#activity {
    height: 395px;
    overflow-y: scroll;
}

.ah {
    height: 485px;
}
</style>