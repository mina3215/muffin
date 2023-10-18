<template>
  <div>
    <!-- 기존의 박스오피스 -->
    <h1 class="section-title">박스오피스 Top 10</h1>
    <div class="row row-cols-1 row-cols-md-5 g-2">
        <BoxOfficeListItem v-for="(movie) in movies" :key="movie.id" :movie="movie" />
    </div>
    <div v-if="genre_3">
        <!-- 첫번째 장르별 추천 영화 -->
        <h1 class="section-title">내가 좋아하는 영화를 좋아요 누른 비슷한 취향의 사람들이 좋아요 누른 이런 영화들은 어떠세요</h1>
        <div class="row row-cols-1 row-cols-md-5 g-2">
          <BoxOfficeListItem v-for="(movie) in recommend_list" :key="movie.id" :movie="movie" />
        </div>
        <br>
        <h1 class="section-title">{{genre_1['genre_name']['name']}}</h1>
        <div class="row row-cols-1 row-cols-md-5 g-2">
          <BoxOfficeListItem v-for="(movie) in genre_1['movies']" :key="movie.id" :movie="movie" />
        </div>
        <br>
        <!-- 두번째 -->
        <h1 class="section-title">{{genre_2['genre_name']['name']}}</h1>
        <div class="row row-cols-1 row-cols-md-5 g-2">
          <BoxOfficeListItem v-for="(movie) in genre_2['movies']" :key="movie.id" :movie="movie" />
        </div>
        <br>
        <!-- 세번째 -->
        <h1 class="section-title">{{genre_3['genre_name']['name']}}</h1>
        <div class="row row-cols-1 row-cols-md-5 g-2">
            <BoxOfficeListItem v-for="(movie) in genre_3['movies']" :key="movie.id" :movie="movie" />
        </div>
      </div>
    </div>
</template>

<script>

import BoxOfficeListItem from '@/components/BoxOfficeListItem'
export default {
  name: 'BoxOfficeList',
  data(){
    return{
      recommend_list : null,
      genre_1 : null,
      genre_2 : null,
      genre_3 : null,
    }
  },
  components: {
    BoxOfficeListItem,
  },
  computed: {
    movies() {
      return this.$store.state.movies
    },
    genres(){
      return this.$store.state.myAccounts.my_genre
    },
    sorted_genres(){
      return this.$store.state.genres_movies
    }
  },
  watch: {
    genres:{
      handler(newValue, oldValue){
        console.log('--------------------',newValue, oldValue)
        this.get_my_genre_movie()
      },
      immediate: true
    },
    sorted_genres:{
      handler(newValue,oldValue){
        console.log(newValue, oldValue)
        if(this.$store.state.genres_movies.length== 3){
          this.get_movies_of_genre()
        }
      },
      immediate: true
    }

  },
  methods:{
    get_my_genre_movie(){
      this.$store.dispatch('getgenremovies')
    },
    get_movies_of_genre(){
      const plz = this.$store.state.genres_movies
      this.recommend_list = this.$store.state.myAccounts.recommend_list
      this.genre_1 = plz[0]
      this.genre_2 = plz[1]
      this.genre_3 = plz[2]
      // console.log('3담김',this.genre_1)
    },

  }

}
</script>

<style scoped>
.section-title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 20px;
  color: white;
  text-shadow: 0px 4px 9px black;
}
h1{
  margin-top: 90px;
  text-align: left;
}
.row {
  margin-bottom: 20px;
}
</style>
