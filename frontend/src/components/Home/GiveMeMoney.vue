<template>
    <v-container style="margin-top: 90px;">
        <v-card class="mb-10">
            <v-card-title class="centered-title"> 
              <h1 style="color: gray;">我很可爱，请给我钱！</h1>
            </v-card-title>
            <br>
            <v-card-text>
              <v-row class="d-flex align-center justify-center"> <!-- 添加Flex对齐类 -->
                <v-col cols="3.5" class="d-flex justify-center align-center"> <!-- 每个v-col分占6份，总共12份 -->
                  <v-img src="../../assets/images/wechat.jpg" max-height="1000" max-width="300" contain></v-img>
                </v-col>
                <v-col cols="5" class="d-flex justify-center align-center"> <!-- 每个v-col分占6份，总共12份 -->
                    <v-img src="../../assets/images/qqnl.png" max-height="1000" max-width="700" contain></v-img>
                  </v-col>
                <v-col cols="3.5" class="d-flex justify-center align-center">
                  <v-img src="../../assets/images/wxmoney.jpg" max-height="1000" max-width="300" contain></v-img>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
    </v-container>
  </template>
  
<script>
export default {
    name: 'GiveMeMoney',
    data() {
        return {
        };
    },
    mounted() {
        this.$store.commit('setAppTitle', '支持我们');
    },
};
</script>

<style scoped>
.centered-title {
  display: flex;
  justify-content: center;
}
</style>