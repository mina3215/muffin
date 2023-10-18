<template>
  <div class="searchboard">
    <div>
      <h1>'{{ keyword }}'의 검색 결과</h1>
      <h3 v-if="movies">총 영화 {{ movies.length }}개,&nbsp;&nbsp;&nbsp;배우 {{ actors.length }}개의 결과가 있음 !</h3>
      <hr class="p-3">
      <div class="results">
        <div>
          <h3>영화 검색 결과</h3>
          <div v-for="movie in movies" :key="movie.id" class="result-item">
            <router-link
              :to="{
                name: 'moviedetail',
                params: { id: movie.id },
              }"
              class="result-link"
            >
              <img :src="getFullImageUrl(movie.poster_path)" class="result-image" alt="Movie Poster" />
              <p class="result-title">{{ movie.title }}</p>
            </router-link>
          </div>
        </div>
        <div>
          <h3>배우 검색 결과</h3>
          <div v-for="actor in actors" :key="actor.id" class="result-item">
            <router-link
              :to="{
                name: 'actordetail',
                params: { id: actor.id },
              }"
              class="result-link"
            >
            <div v-if="actor.id == 314159265359">
             <img src="@/assets/ye.png" style="width: 150px; height: 200px;" class="card-img-top img-fluid" alt="">            
            </div>
             <div v-else>
             <img :src="getFullImageUrl(actor.profile_path)" style="width: 150px; height: 200px;" class="card-img-top img-fluid" alt="..." />
            </div>              <p class="result-title">{{ actor.name }}</p>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
const API_URL = 'http://127.0.0.1:8000/muffins/'
import axios from 'axios'
export default {
  name: 'SearchView',
  data() {
    return {
      movies: [],
      actors: [],
    }
  },
  props: {
    keyword: String,
  },
  mounted() {
    this.get_movie()
  },
  watch: {
    keyword: {
      immediate: true,
      handler(newKeyword) {
        this.get_movie(newKeyword)
      },
    },
  },

  methods: {
    getFullImageUrl(path) {
      if (path) {
        return `https://image.tmdb.org/t/p/original${path}`
      }
      return '' // 이미지 URL이 없는 경우 빈 문자열 반환
    },
    get_movie() {
      const keyword = this.keyword
      axios({
        method: 'get',
        url: `${API_URL}search/${keyword}/`,
      })
        .then((res) => {
          console.log(res.data)
          this.movies = res.data['movies']
          this.actors = res.data['actors']
        })
        .catch((error) => {
          console.log(error)
        })
    },
  },
}
</script>

<style scoped>
.searchboard {
  font-size: 25px;
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

.results {
  display: flex;
  justify-content: center;
}

.result-item {
  flex: 0 0 auto;
  margin-right: 10px;
}

.result-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  text-decoration: none;
  color: #000;
}

.result-image {
  width: 150px;
  height: 200px;
}

.result-title {
  margin-top: 10px;
}
</style>
