const fundpiechart = Vue.createApp({
  template: `
  <div class="shadow-lg p-3 mb-5 bg-white rounded">
    <h1 class="text-center">Fund Portfolio</h1>
    <div class="row d-flex justify-content-center align-content-center">
      <canvas id="piechart" style="width:100%;max-width:700px"></canvas>
    </div>
    <div class="row d-flex justify-content-center align-content-center m-3">
      <button type="button" class="btn btn-primary btn-md btn-block">View all Stocks</button>
    </div>
  </div>`
})
fundpiechart.mount('#fundpiechart')

