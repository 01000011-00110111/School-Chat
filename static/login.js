const checkbox = document.getElementById('checkBox')
  const checkState = window.localStorage.getItem('checkedState')
  const schemeState = window.localStorage.getItem('schemeState')
  const states = [true, false]
  const passwordState = ["visible", "hidden"]
  var currentPasswordState = passwordState[1]
  const passwordButton = document.getElementById("showPswButton")
  const icon = document.getElementById("re")
  const schemeButton = document.getElementById("schemeButton")
  const loginContainer = document.getElementById("loginContainer")
  const leftPanel = document.getElementById("leftPanel")
  const innerContainer = document.getElementById("innerContainer")
  const schemeIcon = document.getElementById("schemeIcon")
  const tos = document.getElementById("tos-body")

  const getcheckedState = () => {
    if (checkState == "true")
    {
      checkbox.checked = states[0]
    }
    else if (checkState == "false")
    {
      checkbox.checked = states[1]
    }
  }
  getcheckedState()

  const showPassword = () => {
    if (currentPasswordState == passwordState[1])
    {
      currentPasswordState = passwordState[0]
      document.getElementById('pswInput').type = 'text'
      icon.classList.add("fa-eye-slash")
      icon.classList.remove("fa-eye")
    }
    else if (currentPasswordState == passwordState[0])
    {
      currentPasswordState = passwordState[1]
      document.getElementById('pswInput').type = 'password'
      icon.classList.remove("fa-eye-slash")
      icon.classList.add("fa-eye")
    }
  }

  checkbox.addEventListener('change', (event) => {
    window.localStorage.setItem("checkedState", event.currentTarget.checked)
  })

  schemeButton.addEventListener('click', (event) => {
    if (event.shiftKey)
    {
      if (!window.localStorage.getItem("flatStyle"))
      {
        window.localStorage.setItem("flatStyle", "false")
      }
      else if (window.localStorage.getItem("flatStyle"))
      {
        if (window.localStorage.getItem("flatStyle") == "false")
        {
          window.localStorage.setItem("flatStyle", "true")
        }
        else if (window.localStorage.getItem("flatStyle") == "true")
        {
          window.localStorage.setItem("flatStyle", "false")
        }
      }
    }
    else 
    {
      if (!schemeState) 
      {
        window.localStorage.setItem("schemeState", "dark")
      }

      if (schemeState == "light")
      {
        window.localStorage.setItem("schemeState", "dark")
      }
      else if (schemeState == "dark")
      {
        window.localStorage.setItem("schemeState", "light")
      }
    }
    window.location.reload()
  })

  const retrieveScheme = () => {
    if (schemeState == "light")
    {
      loginContainer.classList.add("light-mode")
      leftPanel.classList.add("light-mode")
      innerContainer.classList.add("light-mode")
      schemeIcon.classList.add("light-mode")
      schemeIcon.classList.add("fa-moon")
      schemeIcon.classList.remove("fa-sun")
    }
    else if (schemeState == "dark")
    {
      loginContainer.classList.remove("light-mode")
      leftPanel.classList.remove("light-mode")
      innerContainer.classList.remove("light-mode")
    }
  }
  retrieveScheme()

  if (window.localStorage.getItem("flatStyle") == 'true')
  {
    leftPanel.classList.add("flat-style")
    innerContainer.classList.add("flat-style")
  }
  else if (window.localStorage.getItem("flatStyle") == 'false')
  {
    leftPanel.classList.remove("flat-style")
    innerContainer.classList.remove("flat-style")
  }

  socket.on('connect', function () {
    document.getElementById('socket').value = socket.id;
  });

  const tosScroll = (x, y) => {
    tos.scrollTo(x, y)
  }