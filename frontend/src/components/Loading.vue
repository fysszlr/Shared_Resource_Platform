<template>
  <div>
    <v-container fluid class="d-flex align-center justify-center">
      <v-row class="text-center">
        <v-col>
          <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
        </v-col>
      </v-row>
    </v-container>
    <v-container fluid class="d-flex align-center justify-center">
      <v-row class="text-center">
        <v-col>
          <h3>
            {{ motto.title[Math.floor(Math.random() * motto.title.length)] }}
          </h3>
          <h4>
            欢迎回到航U邦。
          </h4>
          <span>正在获取资源站。</span>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  data() {
    return {
      motto: {
        title: [
          '潮平两岸阔，风正一帆悬。',
          '长风破浪会有时，直挂云帆济沧海。',
          '海阔凭鱼跃，天高任鸟飞。',
          '千里之行，始于足下。',
          '路漫漫其修远兮，吾将上下而求索。',
          '不积跬步，无以至千里；不积小流，无以成江海。',
          '天行健，君子以自强不息。',
          '地势坤，君子以厚德载物。',
          '苟日新，日日新，又日新。',
        ],
        subtitle: '欢迎回到航U邦。',
        description: '正在获取资源站。'
      }
    };
  },
}
</script>