<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Http\Resources\UserResource;
use Illuminate\Support\Facades\Log;
use PhpParser\Node\Expr\FuncCall;

class UserController extends Controller
{
    public function showMe(Request $request)
    {
        return new UserResource($request->user());
    }
    public function index()
    {
        $users = \App\Models\User::all();
        return UserResource::collection($users);
    }
    public function update(Request $request, $id)
    {
        $user = \App\Models\User::findOrFail($id);
        $user->update($request->all());
        return new UserResource($user);
    }

    public function getUserTables(Request $request)
    {
        $user = $request->user();
        $tablesString = $user->tables ?? ''; // Obtém a string de tabelas
        $tablesArray = [];
    
        if (!empty($tablesString)) {
            // Divide a string em pares (exemplo: "Dashboard:LineChart,BarChart,PieChart")
            $pairs = explode(';', $tablesString);
            foreach ($pairs as $pair) {
                [$key, $value] = explode(':', $pair) + [null, null];
                if ($key !== null && $value !== null) {
                    // Divide os valores por vírgula e armazena no array
                    $tablesArray[$key] = explode(',', $value);
                }
            }
        }
    
        // Log para depuração
        Log::info('User tables retrieved', ['id' => $user->id, 'tables' => $tablesArray]);
    
        // Retorna as tabelas no formato JSON
        return response()->json(['tables' => $tablesArray]);
    }
}
