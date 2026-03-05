# name:Chidera Agu
# date: 3/4/2026
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 5 (out of 5) --I agree to get 5 points.

import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Movies')

def create_movie():
    user_input = input("Enter a movie title: ")

    response = table.get_item(Key = {"Title":user_input})
    item = response.get("Item")

    if item:
        print("Movie already exists in this database")

    else:
        new_movie = {
            "Title"   : user_input,
            "Ratings" : []
        }
        table.put_item(Item=new_movie)
        print("creating a movie")
    

def print_movie(movie):
    """Print a single movie's details in a readable format."""
    title = movie.get("Title", "Unknown Title")
    year = movie.get("Year", "Unknown Year")
    director = movie.get("Director", "Unknown Director")
    # Ratings is a nested map in the table — handle it gracefully
    ratings = movie.get("Ratings", "No Ratings")
    #rating_str = ", ".join(f"{k}: {v}" for k, v in ratings.items()) if ratings else "No ratings"
    
    print(f"  Title : {title}")
    print(f"  Year  : {year}")
    print(f"  Ratings: {ratings}")
    print(f"  Director: {director}")
    print()



def print_all_movies():
    """Scan the entire Movies table and print each item."""
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No movies found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} movie(s):\n")
    for movie in items:
        print_movie(movie)

class TitleNotFound(Exception):
    pass

def update_rating():
    try:
        title = input("What is the movie title? ")
        response = table.get_item(Key={"Title": title})
        if "Item" not in response:
            raise TitleNotFound("Movie title was not found in database.")
        rating = int(input("What is the rating?: "))
        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Ratings = list_append(Ratings, :r)",
            ExpressionAttributeValues={':r': [rating]})
    except TitleNotFound as e:
        print("Custom error:", e)
    except ValueError:
        print("Input is not a valid integer")
    else:
        print("updating rating")

def delete_movie():
    try:
        title = input("What is the movie title that you would like to delete? ")
        response = table.get_item(Key={"Title":title})
        if "Item" not in response:
            raise TitleNotFound("Movie title was not found in database.")
        table.delete_item(
            Key={'Title': title,})
    except TitleNotFound as e:
        print("Custom error:", e)
    else: 
        print("deleting movie")

def query_movie():
    """
    Prompt user for a Movie Title.
    Print out the average of all ratings in the movie's Ratings list.
    """
    print("query movie")

def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new movie")
    print("Press R: to READ all movies")
    print("Press U: to UPDATE a movie (add a review)")
    print("Press D: to DELETE a movie")
    print("Press Q: to QUERY a movie's average rating")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_movie()
        elif input_char.upper() == "R":
            print_all_movies()
        elif input_char.upper() == "U":
            update_rating()
        elif input_char.upper() == "D":
            delete_movie()
        elif input_char.upper() == "Q":
            query_movie()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
