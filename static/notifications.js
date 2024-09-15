const pushNotification = (sender, message, icon) => {
    createNotification(sender, message, icon);
  
    const remove_notification = () => {
      const notifications = document.getElementsByTagName('notification');
      for (let i = 0; i < notifications.length; i++) {
        notifications[i].remove()
      } 
    }
    setTimeout(remove_notification, 6710)
  }
  
const createNotification = (title, content, img) => {
    const notifcation = document.createElement('notification');
    const notification_title = document.createElement('h4');
    const notification_content = document.createElement('p');
    const content_panel = document.createElement('div');
    const img_panel = document.createElement('div');
    const close_panel = document.createElement('div');
    const close_button = document.createElement('button')
    const icon = document.createElement('img');

    img_panel.classList.add("img_panel");
    content_panel.classList.add("content_panel");
    close_panel.classList.add('close_panel');

    close_button.innerHTML = '<i class="fa-solid fa-x"></i>';
    notification_title.innerHTML = title;
    notification_content.innerHTML = content;
    icon.src = img;

    const end_notification = () => {
        notifcation.style.animationName = "notification_slide_out";
        notifcation.style.animationDuration = ".7s";
    }
        setTimeout(end_notification, 6000)

    close_button.addEventListener('click', () => {
        notifcation.remove()
    });

    document.getElementsByTagName("body")[0].appendChild(notifcation);
    notifcation.appendChild(img_panel);
    notifcation.appendChild(content_panel);
    notifcation.appendChild(close_panel)
    content_panel.appendChild(notification_title);
    content_panel.appendChild(notification_content);
    img_panel.appendChild(icon);
    close_panel.appendChild(close_button);
}