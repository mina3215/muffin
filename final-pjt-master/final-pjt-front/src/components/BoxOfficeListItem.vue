<template>
  <!-- 카드그룹 -->
  <div class="image-container" >
    <div class="col mx-auto"  v-if="$store.state.myAccounts.token">
      <div class="card">
        <router-link
          :to="{
            name: 'moviedetail',
            params: { id: movie.id },
          }"
        >
          <div class="aspect-ratio">
            <img :src="getFullImageUrl(movie.poster_path)"
              class="card-img-top img-fluid"
              alt="..."
            />
          </div>
          <div class="card-body overlay">
            <h5 class="card-title">{{ movie.title }}</h5>
          </div>
        </router-link>
      </div>
    </div>


    <div class="image-container"  v-if="!$store.state.myAccounts.token">
    <div class="col mx-auto">
      <div class="card">
        <img src="@/assets/logo5.png" alt="" class="card-img-top img-fluid">
        <div class="card-body overlay">
        로그인 하세요.
      </div>
      </div>
    </div>
  </div>
  </div>
</template>



<script>
export default {
  name: "BoxOfficeListItem",
  props: {
    movie: Object,
  },
  methods: {
    getFullImageUrl(path) {
      if (path) {
        return `https://image.tmdb.org/t/p/original${path}`;
      }
      return ""; // 이미지 URL이 없는 경우 빈 문자열 반환
    },
  },
};
</script>

<style scoped>
.aspect-ratio {
  position: relative;
  width: 100%;
  padding-top: 150%; /* 조정 가능한 비율 */
}

.aspect-ratio img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-container {
  position: relative;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  opacity: 0;
  transition: opacity 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.image-container:hover .overlay {
  opacity: 1;
}
</style>
