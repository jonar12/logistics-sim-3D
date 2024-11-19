using HTTP
using JSON

function post_request(url::String, json_body::Dict)
    # Convert the JSON body (Dict) to a JSON string
    json_string = JSON.json(json_body)

    # Make the POST request
    response = HTTP.post(url, ["Content-Type" => "application/json"], json_string)

    # Return the response
    return JSON.parse(String(response.body))
end