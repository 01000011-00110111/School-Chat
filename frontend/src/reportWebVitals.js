// Copyright (C) 2023-2025  cserver45, cseven, CastyiGlitchxz
// License info can be viewed in app.py or the LICENSE file inside the github repositiory located here:
// https://github.com/01000011-00110111/School-Chat
const reportWebVitals = onPerfEntry => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(onPerfEntry);
      getFID(onPerfEntry);
      getFCP(onPerfEntry);
      getLCP(onPerfEntry);
      getTTFB(onPerfEntry);
    });
  }
};

export default reportWebVitals;
