function close_loader() {
  const loader =  document.getElementById('loader-show-until-loaded')
  loader.style.backgroundColor = 'rgba(0,0,0,0.0)'
  loader.addEventListener('animationend', function() {
    loader.remove()
  })
  loader.classList.add('animate__animated', 'animate__flipOutX')
  document.getElementById('loader-block-until-loaded').style.display = 'block'
}

function start_loader() {
  const loader =  document.getElementById('loader-show-until-loaded')
  loader.classList.remove('animated', 'zoomOut')
  loader.style.backgroundColor = 'rgba(0,0,0,0.5)'
  loader.style.display = 'block'
  loader.innerHTML = `
    <div class="row h-100 justify-content-center align-items-center">
      <div class="loader-container">
        <div class="loader-item loader-fs-slow">
          <img class="loader-item loader-rs-med" src="https://utils.mitcave.com/loaders/loader_v1/loader_1.png">
        </div>
        <div class="loader-item loader-rs-med">
          <img class="loader-item loader-fs-fast" src="https://utils.mitcave.com/loaders/loader_v1/loader_2.png">
        </div>
        <div class="loader-item loader-fs-med">
          <img class="loader-item loader-rs-fast" src="https://utils.mitcave.com/loaders/loader_v1/loader_3.png">
        </div>
        <div class="loader-item loader-rs-slow">
          <img class="loader-item loader-fs-med" src="https://utils.mitcave.com/loaders/loader_v1/loader_4.png">
        </div>
        <img class="loader-item" src="https://utils.mitcave.com/loaders/loader_v1/loader_logo.png">
      </div>
    </div>
  `
}

window.addEventListener('DOMContentLoaded', () => {
  // console.log('DOM Loaded')
  start_loader()
})

window.addEventListener('load', () => {
  // console.log('Page Loaded')
  close_loader()
})
