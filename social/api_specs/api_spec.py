API_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "Facebook Clone API",
        "version": "1.0.0",
        "description": "API specification for the social app using clean architecture.",
    },
    "servers": [
        {"url": "http://localhost:8000/"},
    ],
    "paths": {
        "/create-post/": {
            "post": {
                "summary": "Create a new post",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/CreatePostRequest"}
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Post created successfully."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        },
        "/create-comment/": {
            "post": {
                "summary": "Create a top-level comment",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/CreateCommentRequest"}
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Comment created successfully."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        },
        "/reply-to-comment/": {
            "post": {
                "summary": "Reply to an existing comment",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ReplyToCommentRequest"}
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Reply posted successfully."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        },
        "/react-to-post/": {
            "post": {
                "summary": "Create or update a reaction on a post",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ReactToPostRequest"}
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Reaction recorded successfully."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        },
        "/react-to-comment/": {
            "post": {
                "summary": "Create or update a reaction on a comment",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ReactToCommentRequest"}
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Reaction recorded successfully."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        },
        "/get-total-reactions/": {
            "get": {
                "summary": "Get the total number of reactions across all content",
                "responses": {
                    "200": {"description": "Total reactions returned."}
                }
            }
        },
        "/get-reaction-metrics/": {
            "get": {
                "summary": "Get reaction metrics for a post",
                "parameters": [
                    {
                        "name": "post_id",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ],
                "responses": {
                    "200": {"description": "Reaction metrics returned."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        },
        "/delete/{post_id}/": {
            "delete": {
                "summary": "Delete a post",
                "parameters": [
                    {
                        "name": "post_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/DeletePostRequest"}
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Post deleted successfully."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        },
        "/get-posts-with-more-positive-reactions/": {
            "get": {
                "summary": "Get posts with more positive reactions than negative or neutral reactions",
                "responses": {
                    "200": {"description": "Posts returned successfully."}
                }
            }
        },
        "/get-posts-reacted-by-user/": {
            "get": {
                "summary": "List posts reacted to by a specific user",
                "parameters": [
                    {
                        "name": "user_id",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ],
                "responses": {
                    "200": {"description": "Posts returned successfully."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        },
        "/get-reactions-to-post/": {
            "get": {
                "summary": "Get all reactions for a given post",
                "parameters": [
                    {
                        "name": "post_id",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ],
                "responses": {
                    "200": {"description": "Reactions returned successfully."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        },
        "/get-post/": {
            "get": {
                "summary": "Retrieve a single post by ID",
                "parameters": [
                    {
                        "name": "post_id",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ],
                "responses": {
                    "200": {"description": "Post returned successfully."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        },
        "/get-user-posts/": {
            "get": {
                "summary": "List posts for a specific user",
                "parameters": [
                    {
                        "name": "user_id",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ],
                "responses": {
                    "200": {"description": "User posts returned successfully."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        },
        "/get-replies-for-comment/": {
            "get": {
                "summary": "Get replies for a comment",
                "parameters": [
                    {
                        "name": "comment_id",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ],
                "responses": {
                    "200": {"description": "Replies returned successfully."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        },
        "/create-group/": {
            "post": {
                "summary": "Create a new group",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/CreateGroupRequest"}
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Group created successfully."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        },
        "/add-member-to-group/": {
            "post": {
                "summary": "Add a member to an existing group",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/AddMemberToGroupRequest"}
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Member added successfully."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        },
        "/remove-member-from-group/": {
            "post": {
                "summary": "Remove a member from a group",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/RemoveMemberFromGroupRequest"}
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Member removed successfully."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        },
        "/make-member-as-admin/": {
            "post": {
                "summary": "Promote a group member to admin",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/MakeMemberAsAdminRequest"}
                        }
                    }
                },
                "responses": {
                    "200": {"description": "Member promoted successfully."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        },
        "/get-group-feed/": {
            "get": {
                "summary": "Get posts from a group feed",
                "parameters": [
                    {"name": "user_id", "in": "query", "required": True, "schema": {"type": "string"}},
                    {"name": "group_id", "in": "query", "required": True, "schema": {"type": "string"}},
                    {"name": "offset", "in": "query", "required": False, "schema": {"type": "integer", "default": 0}},
                    {"name": "limit", "in": "query", "required": False, "schema": {"type": "integer", "default": 10}},
                ],
                "responses": {
                    "200": {"description": "Group feed returned successfully."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        },
        "/get-posts-with-more-comments-than-reactions/": {
            "get": {
                "summary": "Get posts that have more comments than reactions",
                "responses": {
                    "200": {"description": "Posts returned successfully."}
                }
            }
        },
        "/get-silent-group-members/": {
            "get": {
                "summary": "Get group members who have not posted or reacted",
                "parameters": [
                    {"name": "group_id", "in": "query", "required": True, "schema": {"type": "string"}}
                ],
                "responses": {
                    "200": {"description": "Silent group members returned successfully."},
                    "400": {"$ref": "#/components/responses/BadRequest"}
                }
            }
        }
    },
    "components": {
        "schemas": {
            "CreatePostRequest": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "content": {"type": "string"},
                    "group_id": {"type": "string"}
                },
                "required": ["user_id", "content"]
            },
            "CreateCommentRequest": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "post_id": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["user_id", "post_id", "content"]
            },
            "ReplyToCommentRequest": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "comment_id": {"type": "string"},
                    "reply_content": {"type": "string"}
                },
                "required": ["user_id", "comment_id", "reply_content"]
            },
            "ReactToPostRequest": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "post_id": {"type": "string"},
                    "reaction_type": {"type": "string"}
                },
                "required": ["user_id", "post_id", "reaction_type"]
            },
            "ReactToCommentRequest": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "comment_id": {"type": "string"},
                    "reaction_type": {"type": "string"}
                },
                "required": ["user_id", "comment_id", "reaction_type"]
            },
            "DeletePostRequest": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"}
                },
                "required": ["user_id"]
            },
            "CreateGroupRequest": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "name": {"type": "string"},
                    "member_ids": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["user_id", "name"]
            },
            "AddMemberToGroupRequest": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "group_id": {"type": "string"},
                    "new_member_id": {"type": "string"}
                },
                "required": ["user_id", "group_id", "new_member_id"]
            },
            "RemoveMemberFromGroupRequest": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "group_id": {"type": "string"},
                    "member_id": {"type": "string"}
                },
                "required": ["user_id", "group_id", "member_id"]
            },
            "MakeMemberAsAdminRequest": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "group_id": {"type": "string"},
                    "member_id": {"type": "string"}
                },
                "required": ["user_id", "group_id", "member_id"]
            },
            "ErrorResponse": {
                "type": "object",
                "properties": {
                    "error": {"type": "string"}
                },
                "required": ["error"]
            }
        },
        "responses": {
            "BadRequest": {
                "description": "Invalid input or request parameters.",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                    }
                }
            }
        }
    }
}
