const fundstockhistory = Vue.createApp({
  template: `
  <div class="shadow-lg p-3 mb-5 bg-white rounded">
    <h1 class="text-center" style="color:black;">Stock History</h1>
    <div class="row d-flex justify-content-center align-content-center">
      <canvas id="linechart" style="width:100%;max-width:700px"></canvas>
    </div>
    <div class="row d-flex justify-content-center align-content-center m-3">
    </div>
  </div>`
})
fundstockhistory.mount('#fundstockhistory')

