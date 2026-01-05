<template>
  <div>
    <h3>分析步驟</h3>
    <ol class="steps">
      <li>透過 DC wuwa bot 產生聲骸圖片</li>
      <li>將圖片上傳至本工具<br>(可選擇檔案或直接貼上)</li>
      <li>點擊「上傳圖片」開始分析</li>
    </ol>
  </div>
</template>

<style scoped>
.steps {
  padding-left: 20px; 
  margin: 0; 
}
.steps li {
  font-size: 14px;       
  line-height: 1.6;      
}
.steps li::marker {
  font-weight: bold;
  color: #333;
}
</style>