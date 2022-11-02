const loaderComponent = Vue.createApp({});
// Stocks Component
loaderComponent.component("loader", {
  data() {
    return {
        message: 'Welcome to Vue!'
    };
  },
  methods: { },
  template: `
  <div id="mask">
  <div id="popup" class="popup"> 
 <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
   viewBox="0 0 100 100" style="enable-background:new 0 0 100 100;" xml:space="preserve">
<path class="st0" d="M48.8,83.4L20.2,66.9c-0.4-0.2-0.7-0.7-0.7-1.2v-33c0-0.5,0.3-0.9,0.7-1.2l28.6-16.5c0.4-0.2,1-0.2,1.4,0
  l28.6,16.5c0.4,0.2,0.7,0.7,0.7,1.2v33c0,0.5-0.3,0.9-0.7,1.2L50.2,83.4C49.8,83.7,49.2,83.7,48.8,83.4z"/>
<g>
  <defs>
    <path id="SVGID_1_" d="M48.8,82.3L21.2,66.3c-0.4-0.2-0.7-0.7-0.7-1.2V33.2c0-0.5,0.3-0.9,0.7-1.2l27.6-15.9c0.4-0.2,1-0.2,1.4,0
      l27.6,15.9c0.4,0.2,0.7,0.7,0.7,1.2v31.9c0,0.5-0.3,0.9-0.7,1.2L50.2,82.3C49.8,82.5,49.2,82.5,48.8,82.3z"/>
  </defs>
  <clipPath id="SVGID_2_">
    <use xlink:href="#SVGID_1_"  style="overflow:visible;"/>
  </clipPath>
  <g class="st1">
   <g class="cboard"> 
    <path class="st0" d="M66.3,33.3h9.6c2.1,0,3.8,1.7,3.8,3.8v50.8H34.8V37.1c0-2.1,1.7-3.8,3.8-3.8h8.9"/>
    <path class="st2" d="M65.2,37.2H48.6c-1,0-1.7-0.9-1.5-1.9l1.4-7.5c0.1-0.7,0.8-1.3,1.5-1.3h13.7c0.8,0,1.4,0.5,1.5,1.3l1.4,7.5
      C66.9,36.3,66.1,37.2,65.2,37.2z"/>
    <g>
      <polyline class="st3" points="41.1,46.6 42.6,48.1 46.6,44.1"/>
    </g>
    <g>
      <g>
        <line class="st3" x1="41.3" y1="59.3" x2="45.3" y2="55.4"/>
        <line class="st3" x1="45.3" y1="59.3" x2="41.3" y2="55.4"/>
      </g>
    </g>
    <g>
      <polyline class="st3" points="41.1,69.1 42.6,70.5 46.6,66.6"/>
    </g>
    <g>
      <polyline class="st3" points="41.1,80.3 42.6,81.8 46.6,77.8"/>
    </g>
    <g>
      <rect x="57.7" y="43.6" class="st4" width="17" height="2.2"/>
      <rect x="50" y="43.6" class="st4" width="5.9" height="2.2"/>
      <rect x="50" y="47.1" class="st4" width="9.5" height="2.2"/>
      <rect x="61.3" y="47.1" class="st4" width="10.7" height="2.2"/>
    </g>
    <g>
      <rect x="57.7" y="57.9" class="st4" width="8.5" height="2.2"/>
      <rect x="67.6" y="57.9" class="st4" width="7.7" height="2.2"/>
      <rect x="50" y="57.9" class="st4" width="5.9" height="2.2"/>
      <rect x="50" y="54.3" class="st4" width="9.5" height="2.2"/>
      <rect x="61.3" y="54.3" class="st4" width="10.7" height="2.2"/>
    </g>
    <g>
      <rect x="54.7" y="69.4" class="st4" width="13.5" height="2.2"/>
      <rect x="69.6" y="69.4" class="st4" width="5.7" height="2.2"/>
      <rect x="50" y="69.4" class="st4" width="2.9" height="2.2"/>
      <rect x="50" y="65.8" class="st4" width="15.5" height="2.2"/>
      <rect x="67.3" y="65.8" class="st4" width="4.7" height="2.2"/>
    </g>
    <g>
      <rect x="54.7" y="80.4" class="st4" width="13.5" height="2.2"/>
      <rect x="69.6" y="80.4" class="st4" width="5.7" height="2.2"/>
      <rect x="50" y="80.4" class="st4" width="2.9" height="2.2"/>
      <rect x="50" y="76.8" class="st4" width="15.5" height="2.2"/>
      <rect x="67.3" y="76.8" class="st4" width="4.7" height="2.2"/>
    </g>
    </g>
  </g>
</g>
<g>
  <path class="st5" d="M22.3,76.4l0.1-37.7c0-2.4,2.2-4.4,4.9-4.4c2.7,0,4.9,2,4.9,4.4l-0.1,37.8l-4.7,8.2L22.3,76.4z"/>
  <path class="st2" d="M27.3,79.9l-2.5-5.7l0.1-34.3c0-1.3,1.1-2.4,2.4-2.4h0c1.3,0,2.4,1.1,2.4,2.4l-0.1,34.4L27.3,79.9z"/>
  <path class="st2" d="M25,73.3c0,0,2-1,4.4,0"/>
  <line class="st2" x1="24.9" y1="44.4" x2="29.7" y2="44.4"/>
</g> 
</svg> 
  {{message}}
</div>  
</div>
        `,
});

loaderComponent.mount("#loader");
