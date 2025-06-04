function remove_with_fade( element, speed = 500 ) {
  var seconds = speed/1000
  element.style.transition = "opacity "+seconds+"s ease"
  element.style.opacity = 0
  setTimeout(function() {
      element.parentNode.removeChild(element);
  }, speed)
}

function add_with_fade(element, speed = 500) {
  var seconds = speed/1000
  element.style.transition = "opacity "+seconds+"s ease"
  element.style.opacity = 1
  element.style.display = 'block'
}

function close_loader() {
  remove_with_fade(document.getElementById('loader-show-until-loaded'))
  add_with_fade(document.getElementById('loader-block-until-loaded'))
}

function start_loader() {
  const loader =  document.getElementById('loader-show-until-loaded')
  loader.style.backgroundColor = 'rgba(0,0,0,0.5)'
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
