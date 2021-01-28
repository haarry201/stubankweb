/**
 * Copyright (c) 2021
 *
 * StuBank stories system javascript, for navigation between the story elements
 * Credit Adam Argyle https://web.dev/authors/adamargyle/
 *
 * @summary StuBank stories javascript
 * @author Jacob Scase
 *
 * Created at     : 2021-01-26 17:59
 * Last modified  : 2021-01-26 20:25
 */

const stories = document.querySelector('.stories')
const median = stories.offsetLeft + (stories.clientWidth / 2)

const state = {
  current_story: stories.firstElementChild.lastElementChild
}
stories.addEventListener('click', e => {
  if (e.target.nodeName !== 'ARTICLE') 
    return
  
  navigateStories(
    e.clientX > median 
      ? 'next' 
      : 'prev')
})


document.addEventListener('keydown', ({key}) => {
  if (key !== 'ArrowDown' || key !== 'ArrowUp')
    navigateStories(
      key === 'ArrowDown'
        ? 'next'
        : 'prev')
})

const navigateStories = direction => {
  const story = state.current_story
  const lastItemInUserStory = story.parentNode.firstElementChild
  const firstItemInUserStory = story.parentNode.lastElementChild
  const hasNextUserStory = story.parentElement.nextElementSibling
  const hasPrevUserStory = story.parentElement.previousElementSibling
  
  if (direction === 'next') {
    if (lastItemInUserStory === story && !hasNextUserStory)
      return
    else if (lastItemInUserStory === story && hasNextUserStory) {
      state.current_story = story.parentElement.nextElementSibling.lastElementChild
      story.parentElement.nextElementSibling.scrollIntoView({
        behavior: 'smooth'
      })
    }
    else {
      story.classList.add('seen')
      state.current_story = story.previousElementSibling
    }
  }
  else if(direction === 'prev') {
    if (firstItemInUserStory === story && !hasPrevUserStory)
      return
    else if (firstItemInUserStory === story && hasPrevUserStory) {
      state.current_story = story.parentElement.previousElementSibling.firstElementChild
      story.parentElement.previousElementSibling.scrollIntoView({
        behavior: 'smooth'
      })
    }
    else {
      story.nextElementSibling.classList.remove('seen')
      state.current_story = story.nextElementSibling
    }
  }
}

// Wrap every letter in a span
var textWrapper = document.querySelector('.ml2');
textWrapper.innerHTML = textWrapper.textContent.replace(/\S/g, "<span class='letter'>$&</span>");

anime.timeline({loop: true})
  .add({
    targets: '.ml2 .letter',
    scale: [4,1],
    opacity: [0,1],
    translateZ: 0,
    easing: "easeOutExpo",
    duration: 950,
    delay: (el, i) => 70*i
  }).add({
    targets: '.ml2',
    opacity: 0,
    duration: 1000,
    easing: "easeOutExpo",
    delay: 1000
  });


// Wrap every letter in a span
var textWrapper = document.querySelector('.ml9 .letters');
textWrapper.innerHTML = textWrapper.textContent.replace(/\S/g, "<span class='letter'>$&</span>");

anime.timeline({loop: true})
  .add({
    targets: '.ml9 .letter',
    scale: [0, 1],
    duration: 1500,
    elasticity: 600,
    delay: (el, i) => 45 * (i+1)
  }).add({
    targets: '.ml9',
    opacity: 0,
    duration: 1000,
    easing: "easeOutExpo",
    delay: 1000
  });

// Wrap every letter in a span
var textWrapper = document.querySelector('.ml11 .letters');
textWrapper.innerHTML = textWrapper.textContent.replace(/([^\x00-\x80]|\w)/g, "<span class='letter'>$&</span>");

anime.timeline({loop: true})
  .add({
    targets: '.ml11 .line',
    scaleY: [0,1],
    opacity: [0.5,1],
    easing: "easeOutExpo",
    duration: 700
  })
  .add({
    targets: '.ml11 .line',
    translateX: [0, document.querySelector('.ml11 .letters').getBoundingClientRect().width + 10],
    easing: "easeOutExpo",
    duration: 700,
    delay: 100
  }).add({
    targets: '.ml11 .letter',
    opacity: [0,1],
    easing: "easeOutExpo",
    duration: 600,
    offset: '-=775',
    delay: (el, i) => 34 * (i+1)
  }).add({
    targets: '.ml11',
    opacity: 0,
    duration: 1000,
    easing: "easeOutExpo",
    delay: 1000
  });