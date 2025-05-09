<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Firebase\JWT\JWT;

class SupersetController extends Controller
{
    public function getSupersetToken()
    {
        $payload = [
            "user" => [
                "username" => "guest_user",
                "first_name" => "Guest",
                "last_name" => "User",
            ],
            "resources" => [
                ["type" => "dashboard", "id" => "12"]
            ],
            "iat" => time(),
            "exp" => time() + 600, // expira em 10 minutos
        ];

        $secret = env('SUPERSET_SECRET_KEY');
        $jwt = JWT::encode($payload, $secret, 'HS256');

        return response($jwt);
    }
}
