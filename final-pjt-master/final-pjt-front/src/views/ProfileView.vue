<template>
  <div class="ProfileView">
    <h1>프로필</h1>
    
    <div>
      <h3>{{ userinfo.username }} 님의 프로필</h3>
      <!-- 여기를 이름으로 할지.. 아이디로 할지... -->
      <br>
      <span v-if="userinfo" class="followinfo">
        팔로워 : {{ userinfo.follower_cnt }} | 
        팔로잉 : {{ userinfo.followings_cnt }}
      </span>
      
      <div v-if="userinfo.username!==this.$store.state.myAccounts.username">
        <button class="btn btn-primary mt-3" @click="follow">{{ userinfo.is_follow ? '언팔로우' : '팔로우' }}</button>
      </div>
      <br><br>
      <h4>업적</h4>
      <div class="Achievements p-3" v-for="prize in prizes" :key="prize.id">
        <img :src="get_prize_img(prize.id)" alt="">
        {{prize.prize_title}}
      </div>
      <!-- 정보를 가져올 때 팔로우 중인지 그런걸 가져와야 한다 -> 추가해야함. --> 
      
      <div style="display: flex; align-items: center;">
        <h4 style="margin-right: 10px;">좋아요</h4>
      </div>        
      <div style="display: flex; flex-wrap: nowrap;">
        <div v-for="movie in playList" :key="movie.id" style="flex: 0 0 auto; margin-right: 10px;">
          <router-link
            :to="{
              name: 'moviedetail',
              params: { id: movie.id },
            }">
            <img :src="getFullImageUrl(movie.poster_path)" style="width: 150px; height: 200px;" class="card-img-top img-fluid" alt="..." />
          </router-link>
        </div>
      </div>
      <div style="display: flex; align-items: center;">
        <h4 style="margin-right: 10px;">좋아하는 배우</h4>
      </div>
      <div style="display: flex; flex-wrap: nowrap;">
        <div v-for="actor in actors" :key="actor.id" style="flex: 0 0 auto; margin-right: 10px;">
          <router-link
            :to="{
              name: 'actordetail',
              params: { id: actor.id },
            }">
            <div v-if="actor.id == 314159265359">
             <img src="@/assets/ye.png" style="width: 150px; height: 200px;" class="card-img-top img-fluid" alt="">            
           </div>
           <div v-else>
            <img :src="getFullImageUrl(actor.profile_path)" style="width: 150px; height: 200px;" class="card-img-top img-fluid" alt="..." />
          </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios'  
const API_URL = 'http://127.0.0.1:8000/muffins/accounts/profile/'

export default {
name: 'ProfileView',
data(){
  return{
    userinfo : null,
    playList : null,
    prizes : null,
    actors : null

  }
},

created(){
  if(this.$store.state.myAccounts.username){
    this.get_profile()
  }
  else{
    alert('로그인하세요')
  }
},

methods:{
  get_profile(){
    const username = this.$route.params.username

    const requester = this.$store.state.myAccounts.username
    console.log(requester)
    axios({
      method: 'get',
      url: `${API_URL}${username}/${requester}/`
    })
    .then((res) => {

      this.prizes = res.data.prizes
      this.userinfo = res.data.user
      this.playList = res.data.playList
      this.actors = res.data.actors
    })

    
  },
  follow(){
    // this.change_info()
    this.change_info()
    console.log('왔냐?')
    
  },

  change_info(){
    const username = this.$route.params.username
    console.log(typeof(username))
    const user = this.$store.state.myAccounts.username
    console.log(user)
    axios({
      method: 'post',
      url: `${API_URL}${username}/follow/`,
      data:{ "user" : user },
    })
    .then((res) => {
      console.log(res)
      this.userinfo.is_follow = res.data.is_follow
      this.userinfo.follower_cnt = res.data.follower_cnt
    })
    .catch((error)=>{
      console.log(error)
    })
  },
  getFullImageUrl(path) {
    if (path) {
      return `https://image.tmdb.org/t/p/original${path}`
    }
    return "" // 이미지 URL이 없는 경우 빈 문자열 반환
  },
  favorite_genre(){
    {{this.$store.state.sorted_genres}}
  },
  get_prize_img(id){
    return require(`@/assets/prize${id}.png`)
  }  
}
}
</script>
<style scoped>
.ProfileView {
  font-size: 20px;
}

.followinfo {
  color: white;
}

.Achievements {
  align-items: left;
  width: 700px;
  height: auto;
  border: 0.5px solid #dddddd42;
  border-radius: 4px;
  padding: 3px;
  font-size: 20px;
  font-weight: 700;
  text-shadow: 0px 2px 9px rgba(0, 0, 0, 0.336);
  background: linear-gradient(to bottom, #ffffff, #ffffffa9, #ffffff7c);
  margin: auto;
  display: flex; /* 추가 */
  justify-content: flex-start; /* 추가 */
  align-items: center; /* 추가 */
  margin-bottom: 10px; /* 추가 */
}

.Achievements img {
  width: 15%;
  height: 15%;
}

h1 {
  font-size: 38px;
  font-weight: bold;
  margin-bottom: 20px;
  color: white;
  text-shadow: 0px 4px 9px black;
}

h2 {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
  color: white;
  text-shadow: 0px 4px 9px black;
}

h3 {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
  color: white;
  text-shadow: 0px 4px 9px black;
}

h4 {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
  color: white;
  text-shadow: 0px 4px 9px black;
  margin-top: 20px;
}
</style>
