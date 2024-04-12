$("#uploadBtn").on("click", function () {
    var file = $("#fileUpload")[0].files[0];
    uploadFile(file);
})

function uploadFile(file) {
    $.ajax({
        url: 'https://8866ujxfo5.execute-api.us-east-1.amazonaws.com/v1/upload/' + file.name, // Update with your API Gateway endpoint
        type: 'PUT',
        data: file,
        processData: false,
        contentType: false,
        headers: {
            'x-amz-meta-customLabels': $("#custom-tags").val(),
            'x-api-key': 'zXx8zyYojO2Spw71f6B116yuEwnmXFwY57R4NgHf'
        },
        success: function (data) {
            console.log('File uploaded successfully:', data);
        },
        error: function (xhr, status, error) {
            console.error('Error uploading file:', error);
        }
    });
}


var apigClient = apigClientFactory.newClient({
    apiKey: 'zXx8zyYojO2Spw71f6B116yuEwnmXFwY57R4NgHf'
});

$("#searchQuery").on("change", function () {
    const url = new URL(location);
    const url1 = new URL(location);
    url.searchParams.set("q", this.value);
    history.pushState({}, url1, url);
    var params = {
        // This is where any modeled request parameters should be added.
        // The key is the parameter name, as it is defined in the API in API Gateway.
        q: this.value
    };

    var body = {};

    var additionalParams = {};

    apigClient.searchGet(params, body, additionalParams)
    .then(function (result) {
        console.log("here");
        //This is where you would put a success callback
    }).catch(function (result) {
        //This is where you would put an error callback
    });

});

