function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks")
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
} 
document.getElementsByClassName("tablinks")[0].click();

async function fetchVersionTag() {
  try {
      response = await fetch('https://api.github.com/repos/01000011-00110111/School-Chat/tags');
      tags = await response.json();
      filteredTags = tags
      .filter(tag => !tag.name.includes('A'))
      
      // Get the latest tag
      const latestTag = `Beta Version: 1.5-beta.1
      Public Release: ${filteredTags[0]?.name || 'No tags found'}`
      
      // Set the tag name in the <var> element
      document.getElementById('versionText').innerText = latestTag;
  } catch (error) {
      console.error('Error fetching tags:', error);
      document.getElementById('versionText').innerText = 'Error fetching tags';
  }
}

fetchVersionTag();