<template>
  <v-container fluid style="max-width: 90%; margin-top:-90px">
    <v-row justify="space-between">
      <!-- 左侧：统计图 -->
      <v-col cols="4">
        <v-card max-width="600px" class="mt-10 chart-container">
          <div class="chart-title">
            <v-icon left>mdi-certificate</v-icon> 平台发帖情况
          </div>
          <v-divider></v-divider>
          <div ref="chart" class="chart"></div>
        </v-card>
        <!-- todo 再建一个表格 -->
        <v-card max-width="600px" class="mt-10 chart-container">
          <div class="chart-title">
            <v-icon left>mdi-calendar-start</v-icon> 平台最新帖子
          </div>
          <v-data-table :headers="tableHeaders" :items="tableData" item-value="id" hide-default-footer>
            <!-- 自定义 category 列内容 -->
            <template #item.category="{ item }">
              <span>{{ item.category === 0 ? '资源分享' : '任务悬赏' }}</span>
            </template>
          </v-data-table>
        </v-card>
      </v-col>

      <!-- 右侧：公告 -->
      <v-col cols="8">
        <v-expansion-panels accordion v-model="activePanel" class="mt-10">
          <!-- 标题部分 -->
            <v-expansion-panel :disabled="true" :class="$vuetify.theme.dark ? 'announcement-header-dark' : 'announcement-header-light'">
            <v-expansion-panel-header style="justify-content: center;">
              最新公告
            </v-expansion-panel-header>
          </v-expansion-panel>
          <!-- 公告列表 -->
          <v-expansion-panel v-for="(item, i) in news" :key="i">
            <v-expansion-panel-header>
              <div style="display: flex; justify-content: space-between; width: 100%;">
                <div>{{ item.title }}</div>
                <div style="color: grey; text-align: right; margin-right: 16px;">
                  <span>{{ formatDate(item.notified_at) }}</span>
                </div>
              </div>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-md-preview :text="item.content"></v-md-preview>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
        <v-banner v-if="news.length === 0">
          好吧，看起来现在还没有公告。
        </v-banner>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import * as echarts from 'echarts';

import { format } from 'date-fns';

import VMdPreview from '@kangc/v-md-editor/lib/preview';
import '@kangc/v-md-editor/lib/style/preview.css';
import githubTheme from '@kangc/v-md-editor/lib/theme/github.js';
import '@kangc/v-md-editor/lib/theme/style/github.css';
import hljs from 'highlight.js';

VMdPreview.use(githubTheme, {
  Hljs: hljs,
});

export default {
  name: 'BarLineChart',
  components: {
    VMdPreview
  },
  data() {
    return {
      // 表格数据
      tableHeaders: [
        { text: '资源名称', value: 'title' },
        { text: '帖子类别', value: 'category' },
        { text: '菜币', value: 'cost' },
      ],
      tableData: [
        { id: 1, title: '计算机组成课程往年考试', category: 0, cost: '10', username: '张三' },
        { id: 2, title: '资源2', category: 0, cost: '0', username: 'zyt' },
        { id: 3, title: '资源3', category: 1, cost: '12', username: 'wxf' },
        { id: 4, title: '资源4', category: 0, cost: '5', username: 'zlr' },
        { id: 5, title: '资源5', category: 1, cost: '0', username: 'zlr' }
      ],

      chartInstance: null,
      news: [],
      activePanel: 1, // 默认展开第一个面板，设置为数字
      loading: true,
    };
  },
  mounted() {
    this.initChart();
    this.$store.commit("setAppTitle", "首页");
    this.$store.dispatch("getNews", { page: 1 })
      .then(res => {
        this.news = res.messages;
        this.news.sort((a, b) => new Date(b.notified_at) - new Date(a.notified_at));
      })
      .catch(_ => {
        this.news = []; 
        this.$store.commit("setAlert", { type: "error", message: "无法获取公告。请检查你的网络设置。" })
      })
      .finally(() => {
        this.loading = false;
      });
    this.$store.dispatch("getNew")
      .then(res => {
        this.tableData = res;
      })
      .catch(_ => {
        this.$store.commit("setAlert", { type: "error", message: "无法获取最新帖子数据。请检查你的网络设置。" })
      });
  },
  methods: {
    viewDetails(item) {
    },
    formatDate(dateString) {
      return format(new Date(dateString), 'yyyy-MM-dd HH:mm:ss');
    },
    initChart() {
      let resDays = []
      let resNums = []
      this.$store.dispatch("getChart")
      .then(res => {
        resDays = res.days
        resNums = res.nums
        const chartDom = this.$refs.chart;
      this.chartInstance = echarts.init(chartDom);

      const options = {
        title: {
          text: '',
        },
        tooltip: {
          trigger: 'axis',
        },
        xAxis: {
          type: 'category',
          data: resDays,
          axisLabel: {
            rotate: 0,
          },
        },
        yAxis: {
          type: 'value',
        },
        grid: {
          left: '10%',
          right: '10%',
          bottom: '15%',
        },
        series: [
          {
            name: '柱状图',
            type: 'bar',
            data: resNums,
            barWidth: 20,
            itemStyle: {
              color: '#90EE90',
            },
          },
          {
            name: '折线图',
            type: 'line',
            data: resNums,
            itemStyle: {
              color: '#6495ED',
            },
            smooth: true,
            symbol: 'circle',
            symbolSize: 6,
          },
        ],
      };
      this.chartInstance.setOption(options);
      })
      .catch(_ => {
        this.$store.commit("setAlert", { type: "error", message: "无法获取统计图数据。请检查你的网络设置。" })
      });
    },
  },
};
</script>

<style scoped>
.v-expansion-panel-header {
  font-size: large;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.panel-content {
  margin-top: 30px;
}

.chart-container {
  color: #2196f3;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 12.5px;
  margin: 0 auto;
  /* 确保容器靠中 */
}

.chart-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.icon {
  width: 16px;
  height: 16px;
  margin-right: 5px;
}

.chart {
  width: 100%;
  height: 300px;
}

/* 调整标题样式 */
.v-card {
  border: none;
  box-shadow: none;
}

.announcement-header-light {
  background-color: rgb(27, 152, 255) !important;
  /* 天蓝色背景，确保优先级 */
  color: white !important;
  /* 白色字体 */
  text-align: center;
  /* 居中显示 */
  font-size: 80px;
  /* 放大字体 */
  font-weight: bold;
  /* 加粗字体 */
  justify-content: center;
  /* 水平居中内容 */
  display: flex;
  /* 保证水平居中对齐 */
  padding: 0 !important;
  /* 确保没有额外的内边距干扰 */
}

.announcement-header-dark {
  background-color: rgb(17, 18, 87) !important;
  /* 天蓝色背景，确保优先级 */
  color: rgb(255, 255, 255) !important;
  /* 白色字体 */
  text-align: center;
  /* 居中显示 */
  font-size: 80px;
  /* 放大字体 */
  font-weight: bold;
  /* 加粗字体 */
  justify-content: center;
  /* 水平居中内容 */
  display: flex;
  /* 保证水平居中对齐 */
  padding: 0 !important;
  /* 确保没有额外的内边距干扰 */
}

.v-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  margin: 16px 0;
}
</style>