from serpapi import GoogleSearch
import secrets

def suggest_location(search_location):
  params = {
    "engine": "google",
    "q": search_location + " attractions",
    "api_key": secrets.serpapiKey
  }

  search = GoogleSearch(params)
  results = search.get_dict()

  print(results)
  results_string = ""

  if "top_sights" in results:
    top_sights = results['top_sights']['sights']

    print(top_sights)
    sights_suggested = "Suggested places to visit:\n"
    for i in top_sights:
      sights_suggested += i['title'] + '\n'

    print(sights_suggested)
    results_string = sights_suggested
  elif "popular_destinations" in results:
    destinations = results["popular_destinations"]["destinations"]
    destinations_string = "Suggested places to visit:"
    for i in destinations:
      destinations_string += i['title'] + "\n"

    print(destinations_string)
    results_string = destinations_string
  else:
    results_string = "No suggestions found."

  if not results_string.strip():
    results_string = "No suggestions found."
  print("here")
  return results_string

results = suggest_location("usa")
print(results)