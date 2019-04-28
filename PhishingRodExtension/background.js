chrome.webNavigation.onCompleted.addListener(function (details) {
    if (details.url && details.url.match('https://mail.google.com/mail/u/0/#inbox')) {
        function runPyScript(){
            var jqxhr = $.ajax({
                type: "GET",
                url: "/quickStart.py",
                async: false,
            });
        
            return jqxhr.responseText;
        }

        print(runPyScript())
        
        // do something with the response
        response= runPyScript('data to process');
        console.log(response);
        chrome.tabs.executeScript(details.tabId, {
            code: 'alert("Page is done")'
        });
    }
},
{
    url: [{hostContains: '.google.'}]
}
);