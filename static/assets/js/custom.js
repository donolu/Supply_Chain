$("#id_category_name").change(function () {
    const url = $("#productForm").attr("data-subcategory-url");  // get the url of the `getsubcategories` view
    const category_nameId = $(this).val();  // get the selected Category_name ID from the HTML input

    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= /persons/ajax/load-cities/ )
        data: {
            'category_name_id': category_nameId       // add the category id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
            console.log(data);
            $("#id_sub_category").html(data);  // replace the contents of the city input with the data that came from the server
            /*

            let html_data = '<option value="">---------</option>';
            data.forEach(function (city) {
                html_data += `<option value="${city.id}">${city.name}</option>`
            });
            console.log(html_data);
            $("#id_city").html(html_data);

            */
        }
    });

});

function confirmDelete() {
    return confirm('Are you sure you want to delete?');
};

