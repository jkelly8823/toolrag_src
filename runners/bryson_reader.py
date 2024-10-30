# import json

# # # # Sample JSON data
# data = [
#     "```json\n{\n  \"code\": \"#include <stdio.h>\\n#include <string.h>\\n\\nvoid calculateUserScore(char *userName) {\\n    char userData[50];\\n    int userScore = 0;\\n    int maxRetries = 5;\\n    int retryCount = 0;\\n\\n    while (retryCount < maxRetries) {\\n        printf(\\\"Enter user data: \\\");\\n        gets(userData);\\n        userScore += strlen(userData);\\n\\n        if (userScore > 100) {\\n            printf(\\\"User score exceeded limit.\\\\n\\\");\\n            return;\\n        }\\n\\n        retryCount++;\\n    }\\n\\n    printf(\\\"Final user score: %d\\\\n\\\", userScore);\\n}\\n\\nvoid anotherFunction() {\\n    char tempData[30];\\n    strcpy(tempData, \\\"example data\\\");\\n}\\n\"\n}\n```",
#     "```json\n{\n  \"code\": \"\n  #include <stdio.h>\n  #include <stdlib.h>\n  \n  typedef struct {\n    int userAge;\n    double transactionAmount;\n    int isLoggedIn;\n    char *productList;\n    float currentTemperature;\n    int customerFeedbackScore;\n  } UserProfile;\n\n  UserProfile* generateUserProfile(int age, double amount, int isLogged) {\n    UserProfile *profile = (UserProfile *)malloc(sizeof(UserProfile));\n    if (!profile) return NULL;\n  \n    profile->userAge = age;\n    profile->transactionAmount = amount;\n    profile->isLoggedIn = isLogged;\n    \n    profile->productList = (char *)malloc(50 * sizeof(char));\n    if (!profile->productList) {\n      free(profile);\n      return NULL;\n    }\n    \n    printf(\\\"Enter products (up to 100 characters): \\\");\n    char input[100];\n    scanf(\\\"%s\\\", input);\n    \n    for (int i = 0; i < 100; i++) {\n      profile->productList[i] = input[i];\n    }\n    \n    return profile;\n  }\n  \"\n}\n```",
#     "```json\n{\n  \"code\": \"#include <stdlib.h>\\n\\nvoid calculateUserScore(int baseScore, int bonusScore) {\\n    int *userScore = malloc(sizeof(int));\\n    if (userScore == NULL) {\\n        return;\\n    }\\n    *userScore = baseScore + bonusScore;\\n    int *tempScore = malloc(sizeof(int));\\n    if (tempScore == NULL) {\\n        free(userScore);\\n        return;\\n    }\\n    *tempScore = *userScore / 2;\\n    free(userScore);\\n    if (*tempScore > 50) {\\n        userScore = tempScore;\\n    }\\n    for (int i = 0; i < 3; i++) {\\n        int extraPoints = (i + 1) * 5;\\n        *tempScore += extraPoints;\\n    }\\n    printf(\\\"User Score: %d\\\\n\\\", *tempScore);\\n    free(tempScore);\\n}\\n\\nvoid handleSession(int orderCount) {\\n    int sessionDuration = 0;\\n    for (int i = 0; i < orderCount; i++) {\\n        sessionDuration += 10;\\n    }\\n    if (sessionDuration > 50) {\\n        int *temperatureReading = malloc(sizeof(int));\\n        if (temperatureReading != NULL) {\\n            *temperatureReading = sessionDuration;\\n            free(temperatureReading);\\n        }\\n    }\\n}\\n\\nvoid logUserIn() {\\n    int *productID = malloc(sizeof(int));\\n    if (productID != NULL) {\\n        *productID = 101;\\n        free(productID);\\n    }\\n    int isLoggedIn = 1;\\n    if (isLoggedIn) {\\n        handleSession(orderCount);\\n    }\\n}\\n\"\n}\n```",
#     "```json\n{\n  \"code\": \"#include <stdio.h>\\n\\nvoid updateUserProfile() {\\n    int userAge;\\n    int totalScore = 0;\\n    int isActive;\\n    int productList[100];\\n    int currentTemperature;\\n\\n    printf(\\\"Enter your age: \\\");\\n    fscanf(stdin, \\\"%d\\\", &userAge);\\n\\n    printf(\\\"Enter your current temperature: \\\");\\n    fscanf(stdin, \\\"%d\\\", &currentTemperature);\\n\\n    printf(\\\"Enter total score increments: \\\");\\n    int increments;\\n    fscanf(stdin, \\\"%d\\\", &increments);\\n\\n    for(int i = 0; i < increments; i++) {\\n        totalScore += 10;\\n    }\\n\\n    printf(\\\"Total score is: %d\\\\n\\\", totalScore);\\n\\n    if (userAge > 18) {\\n        isActive = 1;\\n    } else {\\n        isActive = 0;\\n    }\\n\\n    printf(\\\"User is active: %d\\\\n\\\", isActive);\\n\\n    for(int j = 0; j < 100; j++) {\\n        productList[j] = j + currentTemperature;\\n    }\\n\\n    printf(\\\"Product List: \\\\\\n\\\");\\n    for(int k = 0; k < 100; k++) {\\n        printf(\\\"%d: %d \\\\\\\", k, productList[k]);\\n    }\\n    printf(\\\"\\\\n\\\");\\n\\n    if (isActive) {\\n        printf(\\\"User is active and can access premium features.\\\\n\\\");\\n    } else {\\n        printf(\\\"User is not active and cannot access premium features.\\\\n\\\");\\n    }\\n\\n    return;\\n}\"\n}\n```",
#     "```json\n{\n  \"code\": \"#include <stdio.h>\\n#include <pthread.h>\\n\\nint userScore = 0;\\nint errorCount = 0;\\n\\nvoid* updateUserScore(void* arg) {\\n    for(int i = 0; i < 1000; i++) {\\n        userScore += 1;\\n    }\\n    return NULL;\\n}\\n\\nvoid* countErrors(void* arg) {\\n    for(int i = 0; i < 500; i++) {\\n        errorCount += 1;\\n    }\\n    return NULL;\\n}\\n\\nvoid calculateUserMetrics(int threadCount) {\\n    pthread_t threads[threadCount];\\n    for(int i = 0; i < threadCount; i++) {\\n        if(i % 2 == 0) {\\n            pthread_create(&threads[i], NULL, updateUserScore, NULL);\\n        } else {\\n            pthread_create(&threads[i], NULL, countErrors, NULL);\\n        }\\n    }\\n    for(int i = 0; i < threadCount; i++) {\\n        pthread_join(threads[i], NULL);\\n    }\\n    printf(\\\"Final User Score: %d\\\\n\\\", userScore);\\n    printf(\\\"Final Error Count: %d\\\\n\\\", errorCount);\\n}\\n\"\n}\n```",
#     "```json\n{\n  \"code\": \"\n#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n\nvoid calculateUserMetrics(char *userInput) {\n    int userAge = 25;\n    double productPrice = 19.99;\n    int totalSales = 0;\n    int userScore = 100;\n    int isLoggedIn = 1;\n\n    char command[256];\n    sprintf(command, \\\"echo User Age: %d; Product Price: %.2f; Total Sales: %d; User Score: %d; Is Logged In: %d; User Input: %s\\\", \n            userAge, productPrice, totalSales, userScore, isLoggedIn, userInput);\n\n    if (isLoggedIn) {\n        printf(\\\"Executing command: %s\\\\n\\\", command);\n        system(command);\n    } else {\n        printf(\\\"User must be logged in to calculate metrics.\\\\n\\\");\n    }\n\n    totalSales += 1;\n\n    if (totalSales > 10) {\n        userScore += 10;\n    }\n\n    if (userAge < 18) {\n        printf(\\\"User is a minor.\\\\n\\\");\n    } else {\n        printf(\\\"User is an adult.\\\\n\\\");\n    }\n\n    printf(\\\"Total Sales: %d\\\\n\\\", totalSales);\n    printf(\\\"Current User Score: %d\\\\n\\\", userScore);\n}\n\nvoid anotherFunction() {\n    char userInput[100];\n    printf(\\\"Enter your input: \\\");\n    fgets(userInput, sizeof(userInput), stdin);\n    calculateUserMetrics(userInput);\n}\n\"\n}\n```",
#     "```json\n{\n  \"code\": \"#include <stdio.h>\\n\\nvoid fetchProductList() {\\n    char productList[5];\\n    for (int i = 0; i <= 5; i++) {\\n        productList[i] = 'A';\\n    }\\n    printf(\\\"Products fetched: %s\\\\n\\\", productList);\\n}\\n\"\n}\n```",
#     "```json\n{\n  \"code\": \"\n  void calculateUserScore(int userScore, int itemCount) {\n      int *itemList = malloc(itemCount * sizeof(int));\n      if (itemList == NULL) {\n          return;\n      }\n      for (int i = 0; i < itemCount; i++) {\n          itemList[i] = i * userScore;\n      }\n      int *temp = malloc(sizeof(int));\n      if (temp == NULL) {\n          free(itemList);\n          return;\n      }\n      *temp = userScore + itemCount;\n      free(itemList);\n      return;\n  }\n  \"\n}\n```",
#     "```json\n{\n  \"code\": \"\n  void calculateUserEngagement(int userAge, double totalSales, int isActive, char **productList, double maxScore, char *startDate) {\n      char *sessionToken = malloc(128);\n      char *userSession = malloc(256);\n      if(isActive) {\n          snprintf(sessionToken, 128, \\\"%d-%s\\\", userAge, startDate);\n      }\n      strcpy(userSession, sessionToken);\n      free(sessionToken);\n      sessionToken = NULL;\n      if(isActive) {\n          sessionToken = malloc(128);\n          strcpy(sessionToken, userSession);\n      }\n      if(maxScore > 100) {\n          totalSales *= 1.1;\n      }\n      snprintf(userSession, 256, \\\"Sales: %.2f\\\", totalSales);\n      free(userSession);\n      free(userSession);\n      userSession = NULL;\n      free(sessionToken);\n  }\n  \"\n}\n```",
#     "```json\n{\n  \"code\": \"#include <stdio.h>\\n#include <string.h>\\n#include <stdbool.h>\\n\\nvoid evaluateUserSession(char *input) {\\n    char buffer[50];\\n    int totalScore = 0;\\n    int userAge = 0;\\n    bool isLoggedIn = false;\\n    char productList[100];\\n    int maxRetries = 5;\\n    float currentTemperature = 0.0;\\n    char filePath[256];\\n    char sessionToken[32];\\n    char searchQuery[100];\\n\\n    if (input != NULL) {\\n        strcpy(buffer, input);\\n        totalScore += strlen(buffer);\\n    }\\n    if (totalScore > maxRetries) {\\n        printf(\\\"Max retries exceeded.\\\\n\\\");\\n        return;\\n    }\\n    userAge = strlen(buffer) % 100;\\n    if (userAge >= 18 && userAge < 65) {\\n        isLoggedIn = true;\\n    }\\n    snprintf(productList, sizeof(productList), \\\"User is %s.\\\\n\\\", isLoggedIn ? \\\"logged in\\\" : \\\"not logged in\\\");\\n    printf(\\\"%s\\\", productList);\\n\\n    if (isLoggedIn) {\\n        for (int i = 0; i < userAge; i++) {\\n            currentTemperature += (float)i;\\n        }\\n        currentTemperature /= userAge;\\n        printf(\\\"Average temperature: %.2f\\\\n\\\", currentTemperature);\\n    }\\n    strncpy(filePath, \\\"/user/data/session.txt\\\", sizeof(filePath) - 1);\\n    filePath[sizeof(filePath) - 1] = '\\\\0';\\n    sprintf(sessionToken, \\\"%s_token\\\", buffer);\\n    printf(\\\"Session token created: %s\\\\n\\\", sessionToken);\\n    if (isLoggedIn) {\\n        printf(\\\"Welcome user!\\\\n\\\");\\n    }\\n    printf(\\\"Search Query: \\\");\\n    fgets(searchQuery, sizeof(searchQuery), stdin);\\n    printf(\\\"You searched for: %s\\\\n\\\", searchQuery);\\n}\\n\"\n}\n```"
# ]

# # Function to clean and parse the JSON data
# def parse_json_data(data):
#     parsed_data = []
#     for item in data:
#         try:
#             # Clean the string
#             cleaned_string = item.split('```json')[1].split('```')[0].strip()

#             # Load the cleaned string as a JSON object
#             json_object = json.loads(cleaned_string)

#             parsed_data.append(json_object)
#         except json.JSONDecodeError as e:
#             print(f"Error decoding JSON: {e}")
#     return parsed_data

# file_path = r'D:\grad_research_2\datasets\bryson_exampleData.json'

# # with open(file_path, 'r') as file:
# #     data = json.load(file)

# # Read and parse the JSON
# parsed_json = parse_json_data(data)
# print('-'*10)
# # Print the parsed output
# for entry in parsed_json:
#     print(entry)
#     print(type(entry))
#     break