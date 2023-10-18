
<template>
  <div class>    
    <h1>Top 10 배우</h1>
    <div class ="row row-cols-1 row-cols-md-5 g-2">
        <ActorList v-for="(actor) in actors" :key="actor.id" :actor="actor" />
    </div>
  </div>
</template>


<script>
// @ is an alias to /src
import axios from 'axios'
import ActorList from '@/components/ActorList'

const API_URL = 'http://127.0.0.1:8000/'
export default {
  name: 'ActorView',
  data(){
    return{
      actors : null,
    }
  },
  components: {
    ActorList,
  },
  created(){
    this.recommend_actors()
  },
  methods : {
    recommend_actors(){
      axios({
        method: 'get',
        url: `${API_URL}muffins/fan_community/actorpage/`,
      })
      .then((res) => {
        console.log(res)
        this.actors = res.data
      })
      .catch((err)=>{
        console.log(err)
      })
    }
    ,
    getFullImageUrl(path) {
      if (path) {
        return `https://image.tmdb.org/t/p/original${path}`;
      }
      return ""; // 이미지 URL이 없는 경우 빈 문자열 반환
    },
  }
}
</script>
<style scoped>
h1{
    font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
  color: white;
  text-shadow: 0px 4px 9px black;
}
</style>
