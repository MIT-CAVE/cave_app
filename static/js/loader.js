function close_loader() {
  document.getElementById('loader-show-until-loaded').remove()
  document.getElementById('loader-block-until-loaded').style.display = 'block'
}

function start_loader() {
  const loader =  document.getElementById('loader-show-until-loaded')
  loader.style.backgroundColor = 'rgba(0,0,0,0.8)'
  loader.style.display = 'block'
  loader.innerHTML = `
  <div class="row h-100 justify-content-center align-items-center">
    <div class="loader-container">
      <div class="spinner-border text-light" role="status">
        <span class="sr-only"></span>
      </div>
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
