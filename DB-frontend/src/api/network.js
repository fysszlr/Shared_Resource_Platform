import axios from "axios";
import store from "../store";

const undefinedErrorHandler = (status, info) => {
  switch (status) {
    case 400:
      return "对不起。看起来你遇到了一些问题。";
    case 401:
      return "对不起。看起来你没有对应的权限。";
    case 403:
      return "对不起。看起来你的令牌已经过期。请重新登录。";
    case 404:
      return "对不起。看起来你迷路了。";
    case 408:
      return "请求错误。";
    case 422:
      return "对不起。看起来你的请求格式出了点错误。重新检查一下你的输入？";
    case 500:
      return "对不起。看起来我们的服务器出了一些问题。";
    case 501:
      return "对不起。看起来这个服务还没有实现。";
    case 502:
      return "对不起。看起来你的网络配置出了一些问题。";
    case 503:
      return "对不起。看起来这个服务暂时不可用。我们正在紧急维护，请稍等。";
    default:
      return "对不起。看起来你遇到了一些问题。这可能是我们导致的问题。请检查你的网络配置，或者与管理员联系。";
  }
};

const definedErrorHandler = (error) => {
  if (error in definedErrorCodes)
    return definedErrorCodes[error];
  else
    return "我们遇到了一些未知的问题。";
}

const definedErrorCodes = {
  100: "我们遇到了未定义的错误。",
  101: "看起来服务器出现了一些问题。",
  102: "请求的格式不正确。",
  103: "发生了网络错误。",
  104: "未找到对应的资源。",
  200: "发生了与用户相关的错误。",
  201: "用户名已被占用。",
  202: "密码太弱，请设置更强的密码。",
  203: "邮箱已被占用。",
  204: "学号与实名不匹配。",
  205: "未找到学生信息。",
  206: "注册时发生其他错误。",
  207: "登录时未找到对应的账号。",
  208: "密码错误，请检查后重试。",
  209: "该用户已被封禁。",
  210: "登录时发生其他错误。",
  211: "未找到对应的用户信息。",
  212: "用户尚未登录。",
  213: "用户已经登录。",
  214: "用户权限不足。",
  300: "发生了与通知相关的错误。",
  301: "未找到对应的通知。",
  400: "发生了与公告相关的错误。",
  401: "公告创建失败。",
  402: "未找到对应的公告。",
  500: "发生了与帖子或任务相关的错误。",
  501: "创建失败。",
  502: "未找到对应的内容。",
  503: "未支付或未提交。",
  504: "提交或评论失败。",
  505: "找不到相关记录。",
  506: "发生其他错误。",
  507: "关闭操作失败。",
  508: "未关闭。",
  600: "发生了与支付相关的错误。",
  601: "菜币余额不足，请充值后重试。",
};


const router = axios.create({
  timeout: 60000,
  withCredentials: true,
});

function no_nil(obj) {
  for (let i in obj) {
    if (obj[i] === null || obj[i] === undefined) {
      delete obj[i];
    }
  }
  return obj;
}


router.interceptors.request.use(
  config => {
    config.data = no_nil(config.data);
    config.params = no_nil(config.params);
    if (config.method === 'post') {
      if (config.multipart) {
        config.headers['Content-Type'] = 'application/x-www-form-multipart';
      } else if (!config.headers['Content-Type']) {
        config.headers['Content-Type'] = 'multipart/form-data';
      } else {
        config.headers['Content-Type'] = 'application/json';
      }
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
)

router.interceptors.response.use(
  response => {
    if (response.status === 200) {
      let res = response.data.content;
      if (res.code != 0) {
        let message = definedErrorHandler(res.code);
        return Promise.reject(message);
      } return Promise.resolve(res.data);
    } else return Promise.reject(response);
  },
  error => {
    const { response } = error;
    if (response) {
      try {
        return Promise.reject(undefinedErrorHandler(response.status, response.data));
      } catch (e) {
        return Promise.reject("对不起。我们遇到了一些未知的问题。");
      }
    } else {
      return Promise.reject("无法连接到服务器。请检查您的网络连接。");
    }
  }
)

export default router;