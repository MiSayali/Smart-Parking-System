<style>
    p{
        font-family:'Courier New', Courier, monospace;
        font-size: 30px;
        color:black;
        margin-top: 5px;
        margin-bottom: 5px;
    }
</style>

<template>
  <div>
    <p><b>Parking Lot: {{ address }}</b></p>
    <p><b>Free spaces on floor 0: {{ freeSpaces0 }}</b></p>
    <p><b>Free spaces on floor 1: {{ freeSpaces1 }}</b></p>
    <p><b>Free spaces on floor 2: {{ freeSpaces2 }}</b></p>

  </div>
</template>

<script>
import axios from 'axios' //library for making http requests

export default {
  data () {
    return {
      polling: null,
      address: '',
      freeSpaces0: 0,
      freeSpaces1: 0,
      freeSpaces2: 0
    }
  },
  methods: {
    updateState () {
      const path = `http://localhost:5000/api/lot`
      axios
        .get(path)
        .then((response) => {
          this.address = response.data.state[0].address
          this.freeSpaces0 = response.data.state[0].floor0
          this.freeSpaces1 = response.data.state[0].floor1
          this.freeSpaces2 = response.data.state[0].floor2
        })
        .catch((error) => {
          console.log(error)
        })
    },
    pollData () {
      this.polling = setInterval(() => {
        this.updateState()
      }, 10000)
    }
  },
  beforeDestroy () {
    clearInterval(this.polling)
  },
  created () {
    this.pollData()
  }
}
</script>
