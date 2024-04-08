$("#uploadBtn").on("click", function() {
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
        headers: { 'x-amz-meta-customLabels': $("#custom-tags").val() },
        success: function(data) {
            console.log('File uploaded successfully:', data);
        },
        error: function(xhr, status, error) {
            console.error('Error uploading file:', error);
        }
    });
}


$("#searchQuery").on("change", function () {
    const url = new URL(location);
    url.searchParams.set("q", this.value);
    history.pushState({}, "", url);
    $.ajax({
        url: 'https://8866ujxfo5.execute-api.us-east-1.amazonaws.com/v1/search?q=' + this.value, // Update with your API Gateway endpoint
        type: 'GET',
        success: function(data) {
            console.log('search:', data);
        },
        error: function(xhr, status, error) {
            console.error('Error uploading file:', error);
        }
    });

});

