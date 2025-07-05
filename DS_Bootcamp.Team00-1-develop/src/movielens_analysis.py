from bs4 import BeautifulSoup
import requests
import pytest
from datetime import datetime
from collections import defaultdict
from collections import Counter
import re

import pytest

class Links:
    def __init__(self, path_to_the_file):
        self.movieId = []
        self.imdbId = []
        self.tmdbId = []
        for row in self.links_file_reader(path_to_the_file):
            self.movieId.append(row[0])
            self.imdbId.append(row[1])
            self.tmdbId.append(row[2])

    def links_file_reader(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()[1: 1001]
            for line in lines:
                yield line.strip().split(',')
    
    def parse_money_value(self,money_str):
        """
        Преобразует строку с денежным значением (например, "$30,000,000 (estimated)") в число.
        """
        try:            
            cleaned_str = ''.join(filter(str.isdigit, money_str))
            return int(cleaned_str)
        except Exception:
            return 0

    def create_links_csv(self, file_name, lower_bound, upper_bound):
        with open(file_name, 'w') as f:
            f.write('movieId,Directors,Budget,Gross worldwide,Runtime,Genres,Title\n')
            movie_list = []
            for i in range(lower_bound, upper_bound):
                movie_list.append(self.movieId[i])
            imdb_data = self.get_imdb(movie_list, ['Director', 'Directors', 'Budget', 'Gross worldwide', 'Runtime',
                                                   'Genres', 'Title'])
            for i in range(len(imdb_data)):
                # movieId
                line = '"' + imdb_data[i][0] + '",'
                # Directors
                if imdb_data[i][1] != 'N/A':
                    line += '"' + imdb_data[i][1][0] + '","'
                elif imdb_data[i][2] != 'N/A':
                    line += '"' + ','.join(imdb_data[i][2]) + '","'
                else:
                    line += '"0","'
                # Budget
                if imdb_data[i][3] == 'N/A':
                    line += '0","'
                else:
                    try:
                        budget_raw = imdb_data[i][3][0]
                        budget = self.parse_money_value(budget_raw)
                        line += str(budget) + '","'
                    except Exception:
                        print(f'Exception on budget {budget_raw}. movieId: {imdb_data[i][0]}')
                        line += '0","'
                # Gross worldwide
                if imdb_data[i][4] == 'N/A':
                    line += '0","'
                else:
                    try:
                        gross_raw = imdb_data[i][4][0]
                        gross = self.parse_money_value(gross_raw)
                        line += str(gross) + '","'
                    except Exception:
                        print(f'Exception on gross {gross_raw}. movieId: {imdb_data[i][0]}')
                        line += '0","'
                # Runtime
                if imdb_data[i][5] == 'N/A':
                    line += '0",'
                else:
                    runtime_raw = imdb_data[i][5][0]
                    try:
                        runtime_parts = runtime_raw.split()
                        total_minutes = 0
                        for j in range(len(runtime_parts)):
                            if 'hour' in runtime_parts[j]:
                                total_minutes += int(runtime_parts[j - 1]) * 60
                            elif 'minute' in runtime_parts[j]:
                                total_minutes += int(runtime_parts[j - 1])
                        line += str(total_minutes) + '",'
                    except Exception:
                        print(f'Exception on runtime {runtime_raw}. movieId: {imdb_data[i][0]}')
                        line += '0",'
                if imdb_data[i][6] == 'N/A':
                    line += '"0",'
                else:
                    line += '"' + ','.join(imdb_data[i][6]) + '",'
                if imdb_data[i][7] == 'N/A':
                    line += '"0"\n'
                else:
                    line += '"' + imdb_data[i][7][0] + '"\n'
                f.write(line)

    def get_imdb(self, list_of_movies, list_of_fields):
        imdb_info = []
        for movie in list_of_movies:
            if movie not in self.movieId:
                raise ValueError(f'{movie} is not present in the list of movieId\'s')
            index = self.movieId.index(movie)
            imdb_link = f'http://www.imdb.com/title/tt{self.imdbId[index].zfill(7)}/'
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
            try:
                response = requests.get(imdb_link, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                current_movie_data = [movie]
                for field in list_of_fields:
                    try:
                        if field == 'Runtime':
                            field_element = soup.find(string=field).parent
                            contents = field_element.find_next_sibling().get_text()
                            current_movie_data.append([contents])
                            continue
                        if field == 'Genres':
                            genres = soup.select_one('div.ipc-chip-list__scroller')
                            contents = [genre.string for genre in genres.contents]
                            current_movie_data.append(contents)
                            continue
                        if field == 'Title':
                            title = soup.find(class_='hero__primary-text').get_text()
                            current_movie_data.append([title])
                            continue
                        field_element = soup.find(lambda tag: tag.get_text() == field)
                        row_element = field_element.parent
                        li_children = row_element.find_all('li')
                        contents = [li_child.get_text() for li_child in li_children]
                        current_movie_data.append(contents)
                    except AttributeError:
                        current_movie_data.append('N/A')
                imdb_info.append(current_movie_data)
            except requests.ConnectionError as e:
                print(f"A Network problem occurred: {e}")
            except requests.Timeout as e:
                print(f"Request timed out: {e}")
            except requests.TooManyRedirects as e:
                print(f"Too many redirects: {e}")
            except requests.RequestException as e:
                print(f"An error occurred: {e}")
        imdb_info.sort(key=lambda x: int(x[0]), reverse=True)
        return imdb_info

    def top_directors(self, n):
        """
        Возвращает:Словарь, где ключи — имена режиссеров, 
        а значения — количество фильмов.
        """
        counter = Counter()
        file_path = "links_data.csv"
        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                lines = f.readlines()[1:]
                for line in lines:
                    fields = line.strip().split('","')
                    if len(fields) < 2:
                        continue
                    directors = fields[1].replace('"', '')
                    directors_list = [d.strip() for d in directors.split(',') if d.strip() and d != '0']
                    counter.update(directors_list)
            return dict(counter.most_common(n))
        except FileNotFoundError:
            print(f"Error: The file `{file_path}` was not found.")
            return {}
        except Exception as e:
            print(f"Error processing `{file_path}`: {e}")
            return {}

    def most_expensive(self, n):
        """
        Возвращает:Словарь, где ключи — названия фильмов, 
        а значения — бюджет.
        """
        file_path = "links_data.csv"
        unsorted_budgets = {}
        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                lines = f.readlines()[1:]
                for line in lines:
                    fields = line.strip().split('","')
                    if len(fields) < 7:
                        continue  
                    try:
                        budget = float(fields[2])
                    except ValueError:
                        budget = 0
                    title = fields[6].strip('"')
                    unsorted_budgets[title] = budget
            budgets = dict(sorted(unsorted_budgets.items(), key=lambda item: item[1], reverse=True)[:n])
            return budgets
        except FileNotFoundError:
            print(f"Error: The file `{file_path}` was not found.")
            return {}
        except Exception as e:
            print(f"Error processing `{file_path}`: {e}")
            return {}

    def most_profitable(self, n):
        """
        Возвращает:Словарь, где ключи — названия фильмов, 
        а значения — прибыль.
        """
        file_path = "links_data.csv"
        unsorted_profits = {}
        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                lines = f.readlines()[1:]
                for line in lines:
                    fields = line.strip().split('","')
                    if len(fields) < 7:
                        continue  
                    try:
                        profit = float(fields[3])
                    except ValueError:
                        profit = 0
                    title = fields[6].strip('"')
                    unsorted_profits[title] = profit
            profits = dict(sorted(unsorted_profits.items(), key=lambda item: item[1], reverse=True)[:n])
            return profits
        except FileNotFoundError:
            print(f"Error: The file `{file_path}` was not found.")
            return {}
        except Exception as e:
            print(f"Error processing `{file_path}`: {e}")
            return {}

    def longest(self, n):
        """
        Возвращает:Словарь, где ключи — названия фильмов,
         а значения — продолжительность в минутах.
        """
        file_path = "links_data.csv"
        unsorted_runtimes = {}
        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                lines = f.readlines()[1:]
                for line in lines:
                    fields = line.strip().split('","')
                    if len(fields) < 7:
                        continue  
                    try:
                        runtime_minutes = int(fields[4])
                    except ValueError:
                        runtime_minutes = 0
                    title = fields[6].strip('"')
                    unsorted_runtimes[title] = runtime_minutes
            runtimes = dict(sorted(unsorted_runtimes.items(), key=lambda item: item[1], reverse=True)[:n])
            return runtimes
        except FileNotFoundError:
            print(f"Error: The file `{file_path}` was not found.")
            return {}
        except Exception as e:
            print(f"Error processing `{file_path}`: {e}")
            return {}

    def top_cost_per_minute(self, n):
        """
        Возвращает:Словарь, где ключи — названия фильмов,
        а значения — стоимость в минуту.
        """
        file_path = "links_data.csv"
        unsorted_costs = {}
        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                lines = f.readlines()[1:]
                for line in lines:
                    fields = line.strip().split('","')
                    if len(fields) < 7:
                        continue  
                    try:
                        runtime_minutes = int(fields[4])
                        budget = float(fields[2])
                    except ValueError:
                        runtime_minutes = 0
                    cost = 0
                    if runtime_minutes != 0:
                        cost = budget / runtime_minutes
                        cost = round(cost, 2)
                    title = fields[6].strip('"')
                    unsorted_costs[title] = cost
            costs = dict(sorted(unsorted_costs.items(), key=lambda item: item[1], reverse=True)[:n])
            return costs
        except FileNotFoundError:
            print(f"Error: The file `{file_path}` was not found.")
            return {}
        except Exception as e:
            print(f"Error processing `{file_path}`: {e}")
            return {}
    
    def shortest(self, n):
        """
        Возвращает:Словарь, где ключи — названия фильмов,
        а значения — продолжительность в минутах.
        """
        file_path = "links_data.csv"
        unsorted_runtimes = {}
        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                lines = f.readlines()[1:]
                for line in lines:
                    fields = line.strip().split('","')
                    if len(fields) < 7:
                        continue  
                    try:
                        runtime_minutes = int(fields[4])
                    except ValueError:
                        runtime_minutes = 0
                    title = fields[6].strip('"')
                    if runtime_minutes > 0:
                        unsorted_runtimes[title] = runtime_minutes
            runtimes = dict(sorted(unsorted_runtimes.items(), key=lambda item: item[1])[:n])
            return runtimes
        except FileNotFoundError:
            print(f"Error: The file `{file_path}` was not found.")
            return {}
        except Exception as e:
            print(f"Error processing `{file_path}`: {e}")
            return {}
    
    def cheapest(self, n):
        """
        Возвращает:Словарь, где ключи — названия фильмов,
        а значения — бюджет.
        """
        file_path = "links_data.csv"
        unsorted_budgets = {}
        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                lines = f.readlines()[1:]
                for line in lines:
                    fields = line.strip().split('","')
                    if len(fields) < 7:
                        continue  
                    try:
                        budget = float(fields[2])
                    except ValueError:
                        budget = 0
                    title = fields[6].strip('"')
                    if budget > 0:
                        unsorted_budgets[title] = budget
            budgets = dict(sorted(unsorted_budgets.items(), key=lambda item: item[1])[:n])
            return budgets
        except FileNotFoundError:
            print(f"Error: The file `{file_path}` was not found.")
            return {}
        except Exception as e:
            print(f"Error processing `{file_path}`: {e}")
            return {}

class Ratings:
    """
    Analyzing data from ratings.csv
    """
    def __init__(self):
        """
        Put here any fields that you think you will need.
        """
        self.ratings = []
        self.movies = {}
        self.count_data=1000
        path_to_the_ratings='../datasets/ratings.csv'
        path_to_the_movie='../datasets/movies.csv'
        count = 0
        try:
            with open (path_to_the_ratings, 'r', encoding='utf-8') as file:
                next(file)
                for line in file:
                    if count >= self.count_data:
                        break
                    columns = line.strip().split(',')
                    if len(columns) == 4 and 0.0 < float(columns[2]) <= 5.0  and columns[0].isdigit() and columns[1].isdigit() and columns[3].isdigit():
                        self.ratings.append({
                            'userId': columns[0],
                            'movieId': columns[1],
                            'rating': columns[2],
                            'timestamp': columns[3]
                        })
                        count += 1
                    else:
                        raise ValueError(path_to_the_ratings)
                if count < self.count_data:
                    raise ValueError(f'File {path_to_the_ratings} contains only {count} lines, but {self.count_data} expected')
                    
            with open (path_to_the_movie, 'r', encoding='utf-8') as file:
                    next(file)
                    for line in file:
                        columns = []
                        line = line.strip()
                        if not line:
                            continue
                        flag = True
                        new_line = ''
                        for let in line:
                            if (let =='"'):
                                flag=not flag
                            elif (flag and let==','):
                                columns.append(''.join(new_line))
                                new_line=''
                            else:
                                new_line += let
                        columns.append(''.join(new_line))

                        if len(columns) == 3 and columns[0].isdigit():
                            self.movies[columns[0]] = columns[1]
                        else:
                            raise ValueError(path_to_the_movie)
        except FileNotFoundError as e:
            print(f'File:  not found: {e.filename}')
            self.ratings = []
            self.movies = {}
        except ValueError as e:
            print(f'Incorrect data in file: {e}')
            self.ratings = []
            self.movies = {}
        except Exception as e:
            print(f'Error while reading file: {e}')
            self.ratings = []
            self.movies = {}

    class Movies:  
        def __init__(self, parent_item):
            self.parent = parent_item

        def dist_by_year(self):
            """
            The method returns a dict where the keys are years and the values are counts. 
            Sort it by years ascendingly. You need to extract years from timestamps.
            """
            if not self.parent.ratings:
                return {}
            ratings_by_year = defaultdict(int)
            try:
                for item in self.parent.ratings:
                    year = datetime.fromtimestamp(int(item['timestamp'])).year
                    ratings_by_year[year] +=1
                
                ratings_by_year = dict(sorted(ratings_by_year.items()))
                return ratings_by_year
            except Exception as e:
                print(f'Error while reading file: {e}')
                return {}

        def dist_by_rating(self):
            """
            The method returns a dict where the keys are ratings and the values are counts.
         Sort it by ratings ascendingly.
            """
            if not self.parent.ratings:
                return {}
            ratings_distribution = defaultdict(int)
            try:
                for item in self.parent.ratings:
                    rating = float(item['rating'])
                    ratings_distribution[rating] +=1
                
                ratings_distribution = dict(sorted(ratings_distribution.items()))
                return ratings_distribution
            except Exception as e:
                print(f'Error while reading file: {e}')
                return {}

        def top_by_num_of_ratings(self, n):
            """
            The method returns top-n movies by the number of ratings. 
            It is a dict where the keys are movie titles and the values are numbers.
     Sort it by numbers descendingly.
            """
            if not self.parent.ratings or not self.parent.movies:
                return {}
            
            rating_count = defaultdict(int)
            try:
                for item in self.parent.ratings:
                    rating_count[item['movieId']] += 1
                if n>len(rating_count):
                    raise ValueError
            
                rating_count = sorted(rating_count.items(),key=lambda x: x[1], reverse=True)[:n]
                top_movies = {}
                for movie_id, count in rating_count:
                    if movie_id in self.parent.movies:
                        top_movies[self.parent.movies[movie_id]] = count
                    else:
                        top_movies[movie_id] = count

                return top_movies
            except ValueError:
                print(f'Value out of range unique films: max >> {len(rating_count)}')
                return {}
            except Exception as e:
                print(f'Error while reading file: {e}')
                return {}
            
        def calculate_median(self, ratings):
            ratings =sorted(ratings)
            n = len(ratings)
            midle = n//2
            if n%2 == 0:
                res = (ratings[midle-1] + ratings[midle]) / 2
            else:
                res = ratings[midle]
            return res
        
        def top_by_ratings(self, n, metric):
            """
            The method returns top-n movies by the average or median of the ratings.
            It is a dict where the keys are movie titles and the values are metric values.
            Sort it by metric descendingly.
            The values should be rounded to 2 decimals.
            """
            if not self.parent.ratings or not self.parent.movies:
                return {}
            movie_rating = defaultdict(list)
            try:
                for item in self.parent.ratings:
                    movie_rating[item['movieId']].append(float(item['rating']))
                
                movie_metrics = {}
                for id, ratings in movie_rating.items():
                    if metric == 'average':
                        movie_metrics[id] = sum(ratings) / len(ratings)
                    elif metric == 'median':
                        movie_metrics[id] = self.calculate_median(ratings)
                    else:
                        raise ValueError('Invalid metric. Use average or median.')
                movie_metrics = sorted(movie_metrics.items(), key = lambda x: x[1], reverse=True)
                if n>len(movie_metrics):
                    raise ValueError(f'Value out of range unique films: max >> {len(movie_rating)}')
                top_movies = {}
                for id, metric_val in movie_metrics[:n]:
                    if id in self.parent.movies:
                        top_movies[self.parent.movies[id]] = round(metric_val, 2)
                    else:
                        raise ValueError(f'Cannot find movie title with id: {id}')
                return top_movies
            except Exception as e:
                print(f'Error while reading file: {e}')
                return {}

        def calculate_variance(self, ratings):
            if not ratings:
                return 0
            mean = sum(ratings)/len(ratings)
            variance = sum((x - mean) ** 2 for x in ratings) / len(ratings)
            return variance
               
        def top_controversial(self, n):
            """
            The method returns top-n movies by the variance of the ratings.
            It is a dict where the keys are movie titles and the values are the variances.
          Sort it by variance descendingly.
            The values should be rounded to 2 decimals.
            """
            if not self.parent.ratings or not self.parent.movies:
                return {}
            movie_rating = defaultdict(list)
            try:
                for item in self.parent.ratings:
                    movie_rating[item['movieId']].append(float(item['rating']))
                
                movie_variance = {}
                for id, ratings in movie_rating.items():
                    movie_variance[id] = self.calculate_variance(ratings)
                    
                movie_variance = sorted(movie_variance.items(), key = lambda x: x[1], reverse=True)
                if n>len(movie_variance):
                    raise ValueError(f'Value out of range unique films: max >> {len(movie_rating)}')
                top_movies = {}
                for id, var_item in movie_variance[:n]:
                    if id in self.parent.movies:
                        top_movies[self.parent.movies[id]] = round(var_item, 2)
                    else:
                        raise ValueError(f'Cannot find movie title with id: {id}')
                return top_movies
            except Exception as e:
                print(f'Error while reading file: {e}')
                return {}

        def top_by_year(self, n):
            if not self.parent.ratings:
                return {}
            top_year = self.dist_by_year()
            if not top_year:
                return {}
            try:
                
                if n>len(top_year):
                    raise ValueError(f'Value out of range unique films: max >> {len(top_year)}')
                top_year = dict(sorted(top_year.items(), key=lambda x: x[1], reverse=True)[:n])
                return top_year
            except Exception as e:
                print(f'Error while reading file: {e}')
                return {}
        def lowest_rating(self, n):
            if not self.parent.ratings or not self.parent.movies:
                return {}
            movie_rating = defaultdict(list)
            try:
                for item in self.parent.ratings:
                    movie_rating[item['movieId']].append(float(item['rating']))
                
                movie_metrics = {}
                for id, ratings in movie_rating.items():
                    movie_metrics[id] = sum(ratings) / len(ratings)
                movie_metrics = sorted(movie_metrics.items(), key = lambda x: x[1], reverse=False)
                if n>len(movie_metrics):
                    raise ValueError(f'Value out of range unique films: max >> {len(movie_rating)}')
                top_movies = {}
                for id, metric_val in movie_metrics[:n]:
                    if id in self.parent.movies:
                        top_movies[self.parent.movies[id]] = round(metric_val, 2)
                    else:
                        raise ValueError(f'Cannot find movie title with id: {id}')
                return top_movies
            except Exception as e:
                print(f'Error while reading file: {e}')
                return {}

    class Users(Movies):
        """
        In this class, three methods should work. 
        The 1st returns the distribution of users by the number of ratings made by them.
        The 2nd returns the distribution of users by average or median ratings made by them.
        The 3rd returns top-n users with the biggest variance of their ratings.
     Inherit from the class Movies. Several methods are similar to the methods from it.
        """
        def __init__(self, parent_item):
            super().__init__(parent_item)

        def dist_by_count(self):
            if not self.parent.ratings:
                return {}
            ratings_by_user = defaultdict(int)
            try:
                for item in self.parent.ratings:
                    user = int(item['userId'])
                    ratings_by_user[user] += 1
                
                ratings_by_user = dict(sorted(ratings_by_user.items(),key = lambda x: x[1], reverse=True))
                return ratings_by_user
            except Exception as e:
                print(f'Error while reading file: {e}')
                return {}
        
        def dist_by_rating(self, metric):
            if not self.parent.ratings or not self.parent.movies:
                return {}
            user_rating = defaultdict(list)
            try:
                for item in self.parent.ratings:
                    user_rating[item['userId']].append(float(item['rating']))
                
                movie_metrics = {}
                for id, ratings in user_rating.items():
                    if metric == 'average':
                        movie_metrics[id] = round(sum(ratings) / len(ratings), 2)
                    elif metric == 'median':
                        movie_metrics[id] = round(self.calculate_median(ratings), 2)
                    else:
                        raise ValueError('Invalid metric. Use average or median.')
                movie_metrics = dict(sorted(movie_metrics.items(), key = lambda x: x[1], reverse=True))
                return movie_metrics
            except Exception as e:
                print(f'Error while reading file: {e}')
                return {}
        
        def top_by_variance(self, n):
            if not self.parent.ratings or not self.parent.movies:
                return {}
            movie_rating = defaultdict(list)
            try:
                for item in self.parent.ratings:
                    movie_rating[item['userId']].append(float(item['rating']))
                
                user_variance = {}
                for id, ratings in movie_rating.items():
                    user_variance[id] = self.calculate_variance(ratings)
                    
                user_variance = sorted(user_variance.items(), key = lambda x: x[1], reverse=True)
                if n>len(user_variance):
                    raise ValueError(f'Value out of range unique users: max >> {len(user_variance)}')
                top_variance = {}
                for id, var_item in user_variance[:n]:
                    if id in self.parent.movies:
                        top_variance[id] = round(var_item, 2)
                return top_variance
            except Exception as e:
                print(f'Error while reading file: {e}')
                return {}

class Movies:
    def __init__(self, path_to_the_file, line_count=1000):
        self.dataset = []
        try:
            self._parse_file(path_to_the_file, line_count)
        except FileNotFoundError as e:
            print(f"File not found: {e.filename}")
        except ValueError as e:
            print(f"Invalid line format: {e}")

    def _parse_file(self, path_to_the_file, line_count):
        with open(path_to_the_file, mode='r', encoding='utf-8') as file:
            next(file)
            for i, line in enumerate(file):
                if i >= line_count:
                    break
                line_data = self._parse_line(line.strip())
                if (len(line_data) != 3) or not (line_data[0].isdigit()):
                    raise ValueError(f"Line {i+1} invalid format")
                line_data.append(self._parse_year(line_data[1]))
                self.dataset.append(tuple(line_data))
    
    def _parse_line(self, line):
        parts = []
        in_quotes = False
        current_part = []
        i = 0

        while i < len(line):
            if line[i] == '"':
                in_quotes = not in_quotes
                i += 1
            elif line[i] == ',' and not in_quotes:
                parts.append(''.join(current_part))
                current_part = []
                i += 1
            else:
                current_part.append(line[i])
                i += 1
        parts.append(''.join(current_part))
        return parts
    
    def _parse_year(self, title):
        year = re.search(r'\((\d{4})\)', title)
        if year is None:
            return None
        return int(year.group(1))
    
    def dist_by_release(self) -> dict[int,int]:
        """
        The method returns a dict where the keys are years and the values are counts. 
        You need to extract years from the titles. Sort it by counts descendingly.
        """  
        release_years = defaultdict(int)

        try:
            for data in self.dataset:
                if len(data) < 4 or data[3] is None:
                    continue
                release_years[data[3]] += 1
            
            return dict(sorted(release_years.items(), key=lambda item: item[1], reverse=True))
        except Exception as e:
            print(f"{self.__class__.__name__}: Error occured: {e}")
            return {}    

    def dist_by_genres(self) -> dict[str,int]:
        """
        The method returns a dict where the keys are genres and the values are counts.
        Sort it by counts descendingly.
        """        
        genre_dict = defaultdict(int)

        try:
            for data in self.dataset:
                genres = data[-1].split('|')
                for genre in genres:
                            genre_dict[genre.strip()] += 1
            return dict(sorted(genre_dict.items(),\
                               key=lambda item: item[1],\
                                  reverse=True))
        except Exception as e:
            print(f"{self.__class__.__name__}: Error occured: {e}")
            return {}

    def most_genres(self, n: int) -> dict[str,int]:
        """
        The method returns a dict with top-n movies where the keys are movie titles and 
        the values are the number of genres of the movie. Sort it by numbers descendingly.
        """
        
        try:
            genres_dict = defaultdict(int)

            for data in self.dataset:
                title = data[1]
                genres = data[-2].split('|')
                genres_dict[title] = len(genres)

            return dict(sorted(genres_dict.items(), \
                               key=lambda item: item[1],\
                                  reverse=True)[:n])
        except Exception as e:
            print(f"{self.__class__.__name__}: Error occured: {e}")
            return {}

    def movies_by_year(self, year: int) -> list:
        """
        The method returns a list of movies released in the year.
        """
        return [data[1] for data in self.dataset if data[3] == year]

class Tags:
    tags = []
    dataset = []
    def __init__(self, path_to_the_file, line_count=1000):
        try:
            self._parse_file(path_to_the_file, line_count)
            self.tags = self._uniq_tags()
        except FileNotFoundError as e:
            print(f"File not found: {e.filename}")
        except ValueError as e:
            print(f"Invalid line format: {e}")

    def _parse_file(self, path_to_the_file, line_count):
        self.dataset = []
        with open(path_to_the_file, mode='r', encoding='utf-8') as file:
            next(file)
            for i, line in enumerate(file):
                if i >= line_count:
                    break
                line_data = self._parse_line(line.strip())
                if (len(line_data) != 4) or not (line_data[0].isdigit()) \
                    or not (line_data[1].isdigit()) or not (line_data[3].isdigit()):
                    raise ValueError(f"Line {i+1} invalid format")
                self.dataset.append(line_data)
    
    def _parse_line(self, line):
        parts = []
        in_quotes = False
        current_part = []
        i = 0

        while i < len(line):
            if line[i] == '"':
                in_quotes = not in_quotes
                i += 1
            elif line[i] == ',' and not in_quotes:
                parts.append(''.join(current_part))
                current_part = []
                i += 1
            else:
                current_part.append(line[i])
                i += 1
        parts.append(''.join(current_part))
        return tuple(parts)

    def _uniq_tags(self) -> list:
        try:
            tags = set()
            for data in self.dataset:
                tags.add(data[2])
            return list(tags)
        except Exception as e:
            print(f"{self.__class__.__name__}: Error occured: {e}")
            return []

    def most_words(self, n: int) -> dict[str, int]:
        """
        Returns top-n tags with most words inside. It is a dict where the
        keys are tags and the values are the number of words inside the tag. 
        Sorted it by numbers descendingly.
        """
        
        tag_word_count = dict()

        for tag in self.tags:
            word_count = len(tag.split())
            tag_word_count[tag] = word_count

        big_tags = sorted(tag_word_count.items(), key=lambda item: item[1], reverse=True)
        
        return dict(big_tags[:n])

    def longest(self, n: int) -> list:
        """
        Returns top-n longest tags in terms of the number of characters.
        It is a list of the tags. Sorted by numbers descendingly.
        """
        
        return sorted(self.tags, key=len, reverse=True)[:n]

    def most_words_and_longest(self, n: int ) -> list:
        """
        The method returns the intersection between top-n tags with most words inside and 
        top-n longest tags in terms of the number of characters.
        Drop the duplicates. It is a list of the tags.
        """
        
        return [tag for tag in self.longest(n) if tag in self.most_words(n)]
        
    def most_popular(self, n: int) -> dict[str, int]:
        """
        The method returns the most popular tags. 
        It is a dict where the keys are tags and the values are the counts.
        Drop the duplicates. Sort it by counts descendingly.
        """
        try:
            popular_tags = defaultdict(int)

            for data in self.dataset:
                tag = data[2].lower()
                popular_tags[tag] += 1

            return dict(sorted(popular_tags.items(), key=lambda x: x[1], reverse=True)[:n])
        except Exception as e:
            print(f"{self.__class__.__name__}: Error occured: {e}")
            return {}

    def tags_with(self, word: str) -> list:
        """
        Returns all unique tags that include the word given as the argument.
        Drop the duplicates. It is a list of the tags. Sorted by names alphabetically.
        """
        return sorted([tag for tag in self.tags if word in tag])
    
    '''Additonal functionality'''
    
    def most_active_users(self, n: int) -> dict[int, int]:
        """
        Returns top-n most active users by id.
        """
        try:
            most_active = defaultdict(int)

            for data in self.dataset:
                user_id = int(data[0])
                most_active[user_id] += 1

            return dict(sorted(most_active.items(), key=lambda x: x[1], reverse=True)[:n])
        except Exception as e:
            print(f"{self.__class__.__name__}: Error occured: {e}")
            return {}
    
    def most_tagged_movies(self, n: int):
        """
        Returns top-n most tagged movies by id.
        """
        try:
            most_tagged = defaultdict(int)

            for data in self.dataset:
                movie_id = int(data[1])
                most_tagged[movie_id] += 1

            return dict(sorted(most_tagged.items(), key=lambda x: x[1], reverse=True)[:n])
        except Exception as e:
            print(f"{self.__class__.__name__}: Error occured: {e}")
            return {}


class Test:    
    @pytest.fixture
    def links_instance(self):
        file_path = "../datasets/links.csv"
        return Links(file_path)

    def test_top_directors_type(self, links_instance):
        result = links_instance.top_directors(2)
        assert isinstance(result, dict), "The method should return a dictionary."

    def test_top_directors_elements_type(self, links_instance):
        result = links_instance.top_directors(2)
        for director, count in result.items():
            assert isinstance(director, str), "The director's name should be a string."
            assert isinstance(count, int), "The number of films must be an integer number."

    def test_top_directors_sorted(self, links_instance):
        result = links_instance.top_directors(2)
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True), "The directors should be sorted in descending order of the number of films."

    def test_most_expensive_type(self, links_instance):
        result = links_instance.most_expensive(2)
        assert isinstance(result, dict), "The method should return a dictionary."

    def test_most_expensive_elements_type(self, links_instance):
        result = links_instance.most_expensive(2)
        for title, budget in result.items():
            assert isinstance(title, str), "The name of the movie should be strictl"
            assert isinstance(budget, float), "The budget must be a float"

    def test_most_expensive_sorted(self, links_instance):
        result = links_instance.most_expensive(2)
        budgets = list(result.values())
        assert budgets == sorted(budgets, reverse=True), "Movies should be sorted in descending order of budget."

    def test_most_profitable_type(self, links_instance):
        result = links_instance.most_profitable(2)
        assert isinstance(result, dict), "The method should return a dictionary."

    def test_most_profitable_elements_type(self, links_instance):
        result = links_instance.most_profitable(2)
        for title, profit in result.items():
            assert isinstance(title, str), "The name of the movie should be a string"
            assert isinstance(profit, float), "The profit must be a float"

    def test_most_profitable_sorted(self, links_instance):
        result = links_instance.most_profitable(2)
        profits = list(result.values())
        assert profits == sorted(profits, reverse=True), "Movies should be sorted in descending order of profit"

    def test_longest_type(self, links_instance):
        result = links_instance.longest(2)
        assert isinstance(result, dict), "The method should return a dictionary"

    def test_longest_elements_type(self, links_instance):
        result = links_instance.longest(2)
        for title, runtime in result.items():
            assert isinstance(title, str), "The name of the movie should be a string"
            assert isinstance(runtime, int), "The duration must be an integer number."

    def test_longest_sorted(self, links_instance):
        result = links_instance.longest(2)
        runtimes = list(result.values())
        assert runtimes == sorted(runtimes, reverse=True), "Movies should be sorted in descending order of duration."
    
    def test_top_cost_per_minute_type(self, links_instance):
        result = links_instance.top_cost_per_minute(2)
        assert isinstance(result, dict), "The method should return a dictionary."

    def test_top_cost_per_minute_type(self, links_instance):
        result = links_instance.top_cost_per_minute(2)
        for title, cost in result.items():
            assert isinstance(title, str), "The name of the movie should be a string"
            assert isinstance(cost, float), "The cost of a minute must be a floating point number."

    def test_top_cost_per_minute_sorted(self, links_instance):
        result = links_instance.top_cost_per_minute(2)
        costs = list(result.values())
        assert costs == sorted(costs, reverse=True), "Movies should be sorted in descending order of cost per minute."

    def test_shortest_type(self, links_instance):
        result = links_instance.shortest(2)
        assert isinstance(result, dict), "The method should return a dictionary."

    def test_shortest_elements_type(self, links_instance):
        result = links_instance.shortest(2)
        for title, runtime in result.items():
            assert isinstance(title, str), "The name of the movie should be a string."
            assert isinstance(runtime, int), "The duration must be an integer number."

    def test_shortest_sorted(self, links_instance):
        result = links_instance.shortest(2)
        runtimes = list(result.values())
        assert runtimes == sorted(runtimes), "Movies should be sorted in ascending order of duration."

    def test_cheapest_type(self, links_instance):
        result = links_instance.cheapest(2)
        assert isinstance(result, dict), "The method should return a dictionary."

    def test_cheapest_elements_type(self, links_instance):
        result = links_instance.cheapest(2)
        for title, budget in result.items():
            assert isinstance(title, str), "The name of the movie should be a string."
            assert isinstance(budget, float), "The budget must be a float."

    def test_cheapest_sorted(self, links_instance):
        result = links_instance.cheapest(2)
        budgets = list(result.values())
        assert budgets == sorted(budgets), "Movies should be sorted in ascending order of budget."

    @pytest.fixture
    def ratings_instance(self):
        return Ratings()

    def test_dist_by_year(self, ratings_instance):
        result = ratings_instance.Movies(ratings_instance).dist_by_year()
        assert isinstance(result, dict), "The method should return a dictionary."
        if result:
            assert all(isinstance(year, int) for year in result.keys()), "Years should be integers."
            assert all(isinstance(count, int) for count in result.values()), "Counts should be integers."
            assert list(result.keys()) == sorted(result.keys()), "Years should be sorted in ascending order."

    def test_dist_by_rating(self, ratings_instance):
        result = ratings_instance.Movies(ratings_instance).dist_by_rating()
        assert isinstance(result, dict), "The method should return a dictionary."
        if result:
            assert all(isinstance(rating, float) for rating in result.keys()), "Ratings should be floats."
            assert all(isinstance(count, int) for count in result.values()), "Counts should be integers."
            assert list(result.keys()) == sorted(result.keys()), "Ratings should be sorted in ascending order."

    def test_top_by_num_of_ratings(self, ratings_instance):
        n = 5
        result = ratings_instance.Movies(ratings_instance).top_by_num_of_ratings(n)
        assert isinstance(result, dict), "The method should return a dictionary."
        if result:
            assert all(isinstance(title, str) for title in result.keys()), "Movie titles should be strings."
            assert all(isinstance(count, int) for count in result.values()), "Counts should be integers."
            assert list(result.values()) == sorted(result.values(), reverse=True), "Movies should be sorted by counts in descending order."

    def test_top_by_ratings(self, ratings_instance):
        n = 5
        for metric in ['average', 'median']:
            result = ratings_instance.Movies(ratings_instance).top_by_ratings(n, metric)
            assert isinstance(result, dict), "The method should return a dictionary."
            if result:
                assert all(isinstance(title, str) for title in result.keys()), "Movie titles should be strings."
                assert all(isinstance(value, float) for value in result.values()), "Metric values should be floats."
                assert list(result.values()) == sorted(result.values(), reverse=True), f"Movies should be sorted by {metric} in descending order."

    def test_top_controversial(self, ratings_instance):
        n = 5
        result = ratings_instance.Movies(ratings_instance).top_controversial(n)
        assert isinstance(result, dict), "The method should return a dictionary."
        if result:
            assert all(isinstance(title, str) for title in result.keys()), "Movie titles should be strings."
            assert all(isinstance(variance, float) for variance in result.values()), "Variances should be floats."
            assert list(result.values()) == sorted(result.values(), reverse=True), "Movies should be sorted by variance in descending order."

    @pytest.mark.parametrize("ratings, expected_median", [
        ([4.0, 4.0, 4.0, 5.0, 5.0, 3.0, 5.0, 4.0, 5.0, 5.0], 4.5),
        ([4.0, 4.0, 4.0, 5.0, 5.0, 3.0, 5.0, 4.0, 5.0], 4.0),
        ([1.0], 1.0),
        ([2.0, 3.0], 2.5),
        ])
    def test_calculate_median(self, ratings, expected_median, ratings_instance):
        if not ratings:
            with pytest.raises(ValueError):
                ratings_instance.Movies(ratings_instance).calculate_median(ratings)
        else:
            assert ratings_instance.Movies(ratings_instance).calculate_median(ratings) == expected_median

    @pytest.fixture
    def users_instance(self, ratings_instance):
        return Ratings().Users(ratings_instance)

    def test_dist_by_count(self, users_instance):
        result = users_instance.dist_by_count()
        assert isinstance(result, dict), "The method should return a dictionary."
        if result:
            assert all(isinstance(user_id, int) for user_id in result.keys()), "User IDs should be integers."
            assert all(isinstance(count, int) for count in result.values()), "Counts should be integers."
            assert list(result.values()) == sorted(result.values(), reverse=True), "Users should be sorted by counts in descending order."

    def test_top_by_variance(self, users_instance):
        n = 5
        result = users_instance.top_by_variance(n)
        assert isinstance(result, dict), "The method should return a dictionary."
        if result:
            assert all(isinstance(user_id, str) for user_id in result.keys()), "User IDs should be strings."
            assert all(isinstance(variance, float) for variance in result.values()), "Variances should be floats."
            assert list(result.values()) == sorted(result.values(), reverse=True), "Users should be sorted by variance in descending order."

    def test_top_by_year_type(self, ratings_instance):
        result = ratings_instance.Movies(ratings_instance).top_by_year(2)
        assert isinstance(result, dict), "The method should return a dictionary."

    def test_top_by_year_elements_type(self, ratings_instance):
        result = ratings_instance.Movies(ratings_instance).top_by_year(2)
        for year, count in result.items():
            assert isinstance(year, int), "The year should be an integer."
            assert isinstance(count, int), "The count should be an integer."

    def test_top_by_year_sorted(self, ratings_instance):
        result = ratings_instance.Movies(ratings_instance).top_by_year(2)
        counts = list(result.values())
        assert counts == sorted(counts, reverse=True), "Years should be sorted in descending order of counts."

    def test_top_by_year_n_greater_than_data(self, ratings_instance):
        result = ratings_instance.Movies(ratings_instance).top_by_year(1000)
        assert isinstance(result, dict), "The method should return a dictionary even if n is greater than the number of years."

    def test_lowest_rating_type(self, ratings_instance):
        result = ratings_instance.Movies(ratings_instance).lowest_rating(2)
        assert isinstance(result, dict), "The method should return a dictionary."

    def test_lowest_rating_elements_type(self, ratings_instance):
        result = ratings_instance.Movies(ratings_instance).lowest_rating(2)
        for title, rating in result.items():
            assert isinstance(title, str), "The movie title should be a string."
            assert isinstance(rating, float), "The rating should be a float."

    def test_lowest_rating_sorted(self, ratings_instance):
        result = ratings_instance.Movies(ratings_instance).lowest_rating(2)
        ratings = list(result.values())
        assert ratings == sorted(ratings), "Movies should be sorted in ascending order of ratings."

    def test_lowest_rating_n_greater_than_data(self, ratings_instance):
        result = ratings_instance.Movies(ratings_instance).lowest_rating(1000)
        assert isinstance(result, dict), "The method should return a dictionary even if n is greater than the number of movies."    

    movies = Movies("../datasets/movies.csv")
    tags = Tags("../datasets/tags.csv")
        
    def  default_test_dict(self, test_dict, key_type = str, value_type = int):
        assert isinstance(test_dict, dict)

        assert all(isinstance(key, key_type) for key in test_dict.keys()), \
            f"Not all keys are {key_type.__name__}."
        
        assert all(isinstance(value, value_type) for value in test_dict.values()), \
            f"Not all values are {value_type.__name__}."
        
        sorted_values = list(test_dict.values())
        assert sorted_values == sorted(sorted_values, reverse=True), \
            "The dictionary should be sorted by values in descending order."
        
        assert len(test_dict.keys()) == len(set(test_dict.keys())), \
            "The dict contains duplicates."

    def default_test_list(self, test_list, elem_type = str):
        assert isinstance(test_list, list)
        assert all(isinstance(elem, elem_type) for elem in test_list), \
            f"Not all keys are {elem_type.__name__}."
        
        assert len(test_list) == len(set(test_list)), \
            "The list contains duplicates."
    
    '''Tests for Movies'''
    def test_movies_dist_by_release(self):
        test_data = self.movies.dist_by_release()

        self.default_test_dict(test_data, key_type=int)

    def test_movies_dist_by_genres(self):

        test_data = self.movies.dist_by_genres()

        self.default_test_dict(test_data)

    def test_movies_most_genres(self):
        test_data = self.movies.most_genres(10)
        assert len(test_data) == 10
        self.default_test_dict(test_data)

    def test_movies_movies_by_year(self):
        test_data = self.movies.movies_by_year(1995)
        self.default_test_list(test_data)
    '''Tests for Tags'''
    def test_tags_most_words(self):
        test_data = self.tags.most_words(10)

        assert len(test_data) == 10
        self.default_test_dict(test_data)

    def test_tags_longest(self):
        test_data = self.tags.longest(10)

        assert len(test_data) == 10
        assert test_data == sorted(test_data, key=len, reverse=True), \
            "The list should be sorted by number of characters in descending order."
        
        self.default_test_list(test_data)

    def test_tags_most_words_and_longest(self):
        test_data = self.tags.most_words_and_longest(10)

        assert len(test_data) <= 10

        self.default_test_list(test_data)

        assert test_data == sorted(test_data, key=len, reverse=True), \
            "The list should be sorted by number of characters in descending order."
    
    def test_tags_most_popular(self):
        test_data = self.tags.most_popular(10)

        assert len(test_data) == 10
        
        self.default_test_dict(test_data)

    def test_tags_most_tagged_movies(self):
        test_data = self.tags.most_tagged_movies(10)

        assert len(test_data) == 10
        
        self.default_test_dict(test_data, key_type=int)
    
    def test_tags_most_active_users(self):
        test_data = self.tags.most_active_users(10)

        assert len(test_data) == 10
        
        self.default_test_dict(test_data, key_type=int)
    
