from policy import Policy
import numpy as np
from random import randint, shuffle, choice, choices
import random  # Để giữ hàm random() nguyên bản




class Policy2210xxx(Policy):
    def __init__(self, policy_id=1):
        assert policy_id in [1, 2], "Policy ID must be 1 or 2"

        if policy_id == 1:
            self.policy = GeneticPolicy()
        elif policy_id == 2:
            self.policy = GeneticPolicyy()

    def get_action(self, observation, info):
        return self.policy.get_action(observation, info)

class GeneticPolicy(Policy):
    """
    Lớp GeneticPolicyy áp dụng thuật toán di truyền để tìm hành động tối ưu trong việc sắp xếp hàng hóa.
    """

    def __init__(self):
        """
        Hàm khởi tạo lớp GeneticPolicyy.
        - population_size: Số lượng cá thể trong mỗi quần thể.
        - generations: Số lần lặp để cải tiến quần thể.
        - mutation_rate: Xác suất xảy ra đột biến trên cá thể.
        """
        self.population_size = 50
        self.generations = 5
        self.mutation_rate = 0.01
        self.penaty = -1000
    def get_action(self, observation, info):
        """
        Sử dụng thuật toán di truyền để chọn hành động tối ưu.
        - observation: Trạng thái của môi trường.
        - info: Thông tin bổ sung từ môi trường.
        """
        # Khởi tạo quần thể với các hành động được tạo ngẫu nhiên
        current_population = [self._generate_random_action(observation) for _ in range(self.population_size)]
        
        # Tiến hành các thế hệ để cải thiện quần thể
        for generation in range(self.generations):
            # Tính toán điểm fitness của mỗi cá thể trong quần thể hiện tại
            fitness_values = [self._calculate_fitness(individual, observation, info) for individual in current_population]
            # Lựa chọn các cá thể tốt nhất
            selected_individuals = self._select_best_individuals(current_population, fitness_values)
            # Lai tạo để tạo ra thế hệ con
            new_generation = self._perform_crossover(selected_individuals)
            # Thực hiện đột biến trên thế hệ con
            current_population = self._apply_mutation(new_generation)
        
        # Chọn cá thể có điểm fitness cao nhất từ thế hệ cuối
        best_individual = current_population[np.argmax(fitness_values)]
        return best_individual

    def _generate_random_action(self, observation):
        """
        Sinh ra một hành động ngẫu nhiên dựa trên trạng thái đầu vào.
        """
        # Lấy danh sách các sản phẩm khả dụng
        available_items = [item for item in observation['products'] if item['quantity'] > 0]

        # Chọn một sản phẩm bất kỳ từ danh sách
        chosen_item = random.choice(available_items)
        item_size = chosen_item['size']
        
        pos_x, pos_y = None, None
        while True:
            # Chọn ngẫu nhiên một kho hàng
            stock_index = random.randint(0, len(observation['stocks']) - 1)
            stock_data = observation['stocks'][stock_index]
            stock_width, stock_height = self._get_stock_size_(stock_data)

            # Bỏ qua các kho không chứa được sản phẩm
            if stock_width < item_size[0] or stock_height < item_size[1]:
                continue
            
            # Dò tìm vị trí phù hợp trong kho
            for x in range(stock_width - item_size[0] + 1):
                for y in range(stock_height - item_size[1] + 1):
                    if self._can_place_(stock_data, (x, y), item_size):
                        pos_x, pos_y = x, y
                        break
                if pos_x is not None and pos_y is not None:
                    break
            if pos_x is not None and pos_y is not None:
                break
        
        return {'stock_idx': stock_index, 'size': item_size, 'position': (pos_x, pos_y)}

    def _calculate_fitness(self, action, observation, info):
        """
        Đánh giá mức độ phù hợp (fitness) của một hành động.
        """
        stock_data = observation['stocks'][action['stock_idx']]
        product_size = action['size']
        pos_x, pos_y = action['position']
        if not self._can_place_(stock_data, (pos_x, pos_y), product_size):
            return -self.penaty  # trả về giá trị vô cùng nhỏ
        stock_width, stock_height = self._get_stock_size_(stock_data)
        stock_area = stock_width * stock_height
        product_area = product_size[0] * product_size[1]
        if stock_area == 0:
            stock_area = 1  # Đề phòng chia cho 0
        #center_x, center_y = stock_width // 2, stock_height // 2
        #distance_to_center = ((pos_x - center_x) ** 2 + (pos_y - center_y) ** 2) ** 0.5

        #utilization_ratio = (product_size[0] * product_size[1]) / (stock_width * stock_height)

        #occupied_area = np.sum(stock_data >= 0)
        total_unused_area = stock_area - product_area
        fitness_score = 0.7 * (1 - total_unused_area / stock_area)

       

        return fitness_score

    def _select_best_individuals(self, population, fitness_scores):
        """
        Lựa chọn các cá thể tốt nhất từ quần thể dựa trên điểm fitness.
        """
        sorted_population = [individual for _, individual in sorted(zip(fitness_scores, population), key=lambda pair: pair[0], reverse=True)]
        return sorted_population[:len(sorted_population) // 2]  # Giữ lại 50% cá thể hàng đầu

    def _perform_crossover(self, selected_individuals):
        """
        Thực hiện lai ghép giữa các cá thể được chọn để tạo thế hệ con.
        """
        offspring = []
        while len(offspring) < self.population_size:
            parent_a, parent_b = random.sample(selected_individuals, 2)
            child = {
                'stock_idx': parent_a['stock_idx'],
                'size': parent_b['size'],
                'position': parent_a['position']
            }
            offspring.append(child)
        return offspring

    def _apply_mutation(self, offspring):
        """
        Áp dụng đột biến trên thế hệ con.
        """
        for individual in offspring:
            if random.random() < self.mutation_rate:
                mutated_size = list(individual['size'])
                mutated_size[0] += random.randint(-1, 1)
                mutated_size[1] += random.randint(-1, 1)
                individual['size'] = tuple(mutated_size[::-1])  # Đảo chiều để tăng ngẫu nhiên
        return offspring

    
    
    
    
class GeneticPolicyy(Policy):
    def __init__(self, population_size=90, generations=9, mutation_rate=0.001, penaty=0.3):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.parent1 =[]
        self.parent2 =[]
        self.penaty = penaty
    def get_action(self, observation, info):
        population = [self.random_action(observation) for _ in range(self.population_size)]
        for _ in range(self.generations):
            fitness_scores = [self.evaluate_fitness(action, observation, info) for action in population]
            selected = self.select_population(population, fitness_scores)
            offspring = self.crossover(selected)
            population = self.mutate(offspring)
        best_action = population[np.argmax(fitness_scores)]
        return best_action

    def random_action(self, observation):
        available_products = [product for product in observation['products'] if product['quantity'] > 0]

        selected_product = random.choice(available_products)
        size = selected_product['size']

        pos_x, pos_y = None, None
        while True:
            stock_idx = random.randint(0, len(observation['stocks']) - 1)
            stock = observation['stocks'][stock_idx]
            stock_w, stock_h = self._get_stock_size_(stock)
            if (stock_w >= size[0]) and (stock_h >= size[1]):
                
                for i in range(stock_w - size[0] + 1):
                    for j in range(stock_h - size[1] + 1):
                        if self._can_place_(stock, (i, j), size):
                            
                            pos_x, pos_y = i, j
                            break
                    if pos_x is not None and pos_y is not None:
                        break
                if pos_x is not None and pos_y is not None:
                    break
            if (stock_w >= size[1]) and (stock_h >= size[0]):
                for i in range(stock_w - size[1] + 1):
                    for j in range(stock_h - size[0] + 1):
                        if self._can_place_(stock, (i, j), size[::-1]):
                            size = size[::-1]
                            pos_x, pos_y = i, j
                            break
                    if pos_x is not None and pos_y is not None:
                        break
                if pos_x is not None and pos_y is not None:
                    break
                
        return {'stock_idx': stock_idx, 'size': size, 'position': (pos_x, pos_y)}

    def evaluate_fitness(self, action, observation, info):
        stock_data = observation['stocks'][action['stock_idx']]
        product_size = action['size']
        pos_x, pos_y = action['position']
        if not self._can_place_(stock_data, (pos_x, pos_y), product_size):
            return -2000  # trả về giá trị vô cùng nhỏ
        stock_width, stock_height = self._get_stock_size_(stock_data)
        stock_area = stock_width * stock_height
        product_area = product_size[0] * product_size[1]
        if stock_area == 0:
            stock_area = 1
        total_unused_area = stock_area - product_area
        
        demand = [product['quantity'] for product in observation['products']]
        product_sizes = [product['size'] for product in observation['products']]

    # Sản phẩm được đáp ứng (dựa trên hành động hiện tại)
        provided = np.zeros(len(demand))
        for idx, size in enumerate(product_sizes):
            if (product_size == size).all() or (product_size[::-1] == size).all():
                provided[idx] += 1  # Cung cấp một sản phẩm từ hành động
            break

    # Tính số lượng sản phẩm không được đáp ứng
        unsupplied_sum = 0
        for i, d in enumerate(demand):
            unsupplied = max(0, d - provided[i])
            unsupplied_sum += unsupplied * product_sizes[i][0] * product_sizes[i][1]
        fitness_score = 0.7 * (1 - total_unused_area / stock_area) - self.penaty * (unsupplied_sum / sum(demand))
        return fitness_score


    def select_population(self, population, fitness_scores):
        sorted_population = [action for _, action in sorted(zip(fitness_scores, population), key=lambda x: x[0], reverse=True)]
        return sorted_population[:len(sorted_population)//2]

   
    
    def crossover(self, selected):
        offspring = []
        while len(offspring) < self.population_size:
            parent1, parent2 = random.sample(selected, 2)
            num = random.random()
            if num < 0.25:
                child = {
                    'stock_idx': parent1['stock_idx'],
                    'size': parent1['size'],
                    'position': parent1['position']
                }
            if 0.25 <= num < 0.5:
                child = {
                    'stock_idx': parent2['stock_idx'],
                    'size': parent1['size'],
                    'position': parent2['position']
                }
            if 0.5<= num < 0.75:
                child = {
                    'stock_idx': parent1['stock_idx'],
                    'size': parent2['size'],
                    'position': parent1['position']
                }
            else:
                child = {
                    'stock_idx': parent2['stock_idx'],
                    'size': parent2['size'],
                    'position': parent2['position']
                }
            offspring.append(child)
        return offspring

    def mutate(self, offspring):
        for action in offspring:
            if random.random() < self.mutation_rate:
                mutation_type = random.choice(['size', 'position'])
                if mutation_type == 'size':
                    size = list(action['size'])
                    size[0] += random.randint(-1, 1)
                    size[1] += random.randint(-1, 1)
                    action['size'] = tuple(max(1, x) for x in size)  # Đảm bảo kích thước hợp lệ
                elif mutation_type == 'position':
                    pos_x, pos_y = action['position']
                    pos_x += random.randint(-1, 1)
                    pos_y += random.randint(-1, 1)
                    action['position'] = (max(0, pos_x), max(0, pos_y))
                
        return offspring
    