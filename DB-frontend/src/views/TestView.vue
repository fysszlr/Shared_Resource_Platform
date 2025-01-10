<template>
  <v-container fluid style="max-width: 90%;">
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
            <v-icon left>mdi-certificate</v-icon> 平台最新帖子
          </div>
          <v-data-table
          :headers="tableHeaders"
          :items="tableData"
          item-value="id"
          hide-default-footer
        >
        </v-data-table>
        </v-card>
      </v-col>

      <!-- 右侧：公告 -->
      <v-col cols="8">
        <v-expansion-panels accordion v-model="activePanel" class="mt-10">
          <!-- 标题部分 -->
          <v-expansion-panel :disabled="true" class="announcement-header">
            <v-expansion-panel-header>
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
        { text: '费用or报酬', value: 'cost' },
      ],
      tableData: [
          { id: 1, title: '计算机组成课程往年考试', category: '资源分享', cost: '10', username: '张三'},
          { id: 2, title: '资源2', category: '任务悬赏', cost: '0', username: 'zyt'  },
          { id: 3, title: '资源3', category: '任务悬赏', cost: '12', username: 'wxf' },
          { id: 4, title: '资源4', category: '资源分享', cost: '5', username: 'zlr' },
          { id: 5, title: '资源5', category: '资源分享', cost: '0', username: 'zlr' }
      ],

      chartInstance: null,
      news: [
        {
          title: '公告标题',
          content: `**公告内容**是的，你可以采用这种方式，使用一个简单的 v-expansion-panels 结构，并通过样式控制其展开时的行为，避免内容和大小的变化。这样的做法也非常简洁，并且能避免展开时尺寸的变化。样式调整
你可以通过 v-col 的 cols 和 md 属性来调整统计图和公告的宽度比例。例如，上述代码中，cols="12" md="6" 表示在小屏幕下占据一整行，在中等及以上屏幕下各占一半。

### 注意事项
响应式布局：v-col 默认是响应式的，可以根据屏幕宽度自动调整布局。
高度控制：如果统计图和公告内容高度差异过大，可以通过样式控制高度一致，或在需要时添加滚动条（overflow-y: auto）。
数据加载逻辑：确保两个组件的数据独立加载互不影响，避免加载延迟造成页面布局问题。
通过这种方式，你可以实现整洁的布局效果，同时确保内容对用户友好和清晰展示。`,
          notified_at: '2021-12-01 12:00:00',
        },
        {
          title: '公告标题',
          content: '公告内容',
          notified_at: '2021-12-01 12:00:00',
        },
        {
          title: '公告标题3',
          content: '公告内容3',
          notified_at: '2021-12-02 12:00:00',
        },
        {
          title: '公告标题4',
          content: '公告内容4',
          notified_at: '2021-12-03 12:00:00',
        },
        {
          title: '公告标题5',
          content: '公告内容5',
          notified_at: '2021-12-04 12:00:00',
        },
        {
          title: '公告标题6',
          content: '公告内容6',
          notified_at: '2021-12-05 12:00:00',
        },
        {
          title: '公告标题7',
          content: '公告内容7',
          notified_at: '2021-12-06 12:00:00',
        },
        {
          title: '公告标题8',
          content: '公告内容8',
          notified_at: '2021-12-07 12:00:00',
        },
        {
          title: '公告标题9',
          content: '公告内容9',
          notified_at: '2021-12-08 12:00:00',
        },
        {
          title: '公告标题10',
          content: '公告内容10',
          notified_at: '2021-12-09 12:00:00',
        },
        {
          title: '公告标题11',
          content: '公告内容11',
          notified_at: '2021-12-10 12:00:00',
        },
        {
          title: '公告标题12',
          content: '公告内容12',
          notified_at: '2021-12-11 12:00:00',
        },
        {
          title: '公告标题13',
          content: '公告内容13',
          notified_at: '2021-12-12 12:00:00',
        },
        {
          title: '公告标题14',
          content: '公告内容14',
          notified_at: '2021-12-13 12:00:00',
        },
      ],
      activePanel: 1, // 默认展开第一个面板，设置为数字
      loading: true,
    };
  },
  mounted() {
    this.initChart();
    this.$store.commit("setAppTitle", "公告");
    this.$store.dispatch("getNews", { page: 1 })
      .then(res => {
        this.news = res.messages;
      })
      .catch(_ => {
        this.news = [];
        this.$store.commit("setAlert", { type: "error", message: "无法获取公告。请检查你的网络设置。" })
      })
      .finally(() => {
        this.loading = false;
      });
  },
  methods: {
    viewDetails(item) {
    },
    formatDate(dateString) {
      return format(new Date(dateString), 'yyyy-MM-dd HH:mm:ss');
    },
    initChart() {
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
          data: ['12-01', '12-02', '12-03', '12-04', '12-05', '12-06', '12-07'],
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
            data: [60, 40, 80, 60, 70, 80, 90],
            barWidth: 20,
            itemStyle: {
              color: '#90EE90',
            },
          },
          {
            name: '折线图',
            type: 'line',
            data: [60, 40, 100, 70, 70, 80, 90],
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
  color: #000;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 12.5px;
  background: #fff;
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
  background-color: #000;
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

.announcement-header {
  background-color: #2196f3 !important;
  /* 天蓝色背景，确保优先级 */
  color: white !important;
  /* 白色字体 */
  text-align: center;
  /* 居中显示 */
  font-size: 80px;
  /* 放大字体 */
  font-weight: bold;
  /* 加粗字体 */
}

.announcement-header .v-expansion-panel-header {
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