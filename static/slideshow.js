function handleSlideshowEvent(data) {
  $('.slideshow.item').removeClass('selected')
  $(`.slideshow.item:eq(${data.image_source_index})`).addClass('selected')
}
