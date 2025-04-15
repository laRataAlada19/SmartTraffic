<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UpdateLocationRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }
    
    public function rules(): array
    {
        return [
            'location' => 'nullable|required|string|max:100',
            'direction' => 'nullable|required|string|max:50',
        ];
    }
}
