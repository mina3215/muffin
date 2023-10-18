<template>
  <div>
    <div class="star-rating space-x-4 mx-auto">
      <input type="radio" id="5-stars" name="rating" value="5" v-model="score" />
      <label for="5-stars" class="star pr-4">★</label>
      <input type="radio" id="4-stars" name="rating" value="4" v-model="score" />
      <label for="4-stars" class="star">★</label>
      <input type="radio" id="3-stars" name="rating" value="3" v-model="score" />
      <label for="3-stars" class="star">★</label>
      <input type="radio" id="2-stars" name="rating" value="2" v-model="score" />
      <label for="2-stars" class="star">★</label>
      <input type="radio" id="1-star" name="rating" value="1" v-model="score" />
      <label for="1-star" class="star">★</label>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StarScore',
  props: {
    value: {
      type: Number,
      required: true
    }
  },
  computed: {
    score: {
      get() {
        return this.value;
      },
      set(newValue) {
        this.$emit('input', newValue);
      }
    }
  }
};
</script>

<style>
.star-rating {
  display: flex;
  flex-direction: row-reverse;
  font-size: 2.25rem;
  line-height: 2.5rem;
  justify-content: space-around;
  padding: 0 0.2em;
  text-align: center;
  width: 5em;
}

.star-rating input {
  display: none;
}

.star-rating label {
  -webkit-text-fill-color: transparent;
  -webkit-text-stroke-width: 2.3px;
  -webkit-text-stroke-color: #ffb348c2;
  cursor: pointer;
}

.star-rating :checked ~ label {
  -webkit-text-fill-color: #f6c900;
}

.star-rating label:hover,
.star-rating label:hover ~ label {
  -webkit-text-fill-color: #f6c900;
}
</style>
